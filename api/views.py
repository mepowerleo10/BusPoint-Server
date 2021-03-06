import csv
import io
import json
import os
import math

from decimal import *

import overpy
from django.core import serializers
from django.conf import settings
from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, JsonResponse)
from django.shortcuts import render, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics

from haversine import haversine, haversine_vector, Unit

from .models import Route, Stop, Journey, StopWeight, StopInfo, Feedback
from .serializers import RouteSerializer, StopSerializer, JourneySerializer


class StopViewSet(viewsets.ModelViewSet):
    queryset = Stop.objects.all().order_by('name')
    serializer_class = StopSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().order_by('name')
    serializer_class = RouteSerializer

def upload_stops(request):
    stops_file_name = "api/stops_dodoma.csv"
    stops_file = open(os.path.join(settings.BASE_DIR, stops_file_name), "r")
    data_set = stops_file.read()
    io_string = io.StringIO(data_set)
    next(io_string)
    for col in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Stop.objects.update_or_create(
            name=col[2],
            lat=col[3],
            lon=col[4]
        )
    return HttpResponse("Data set loaded")

@xframe_options_exempt
def get_route(request):
    if request.method != "GET":
        return HttpResponseNotAllowed("Methods other than GET not allowed")

    start_stop = (request.GET['start_lat'],request.GET['start_lon'])
    final_stop = (request.GET['final_lat'],request.GET['final_lon'])

    from_loc = request.GET['from']
    to_loc = request.GET['to']
    
    if (start_stop == None) or (final_stop == None):
        return HttpResponseBadRequest("Start and/or Final stops not set")

    overpassApi = overpy.Overpass()

    # fetch the real lat and lon
    start_stop, final_stop = getStartAndFinalStops(start_stop, overpassApi, final_stop)

    # find the origin route
    start_route = Route.objects.filter(bus_stops__lat=start_stop[0])
    start_route = start_route.filter(bus_stops__lon=start_stop[1]).first()

    # find the destination route
    final_route = Route.objects.filter(bus_stops__lat=final_stop[0])
    final_route = final_route.filter(bus_stops__lon=final_stop[1]).first()

    print("Start Route: ", start_route)
    print("Final Route: ", final_route)
    
    if (start_route == None) or (final_route == None):
        raise Http404("Start/Final Stop not in any route")

    # the stops are in a route, calculate the waypoints
    common_stops = []
    mid_stop = None

    common_stops = start_route.bus_stops.filter(pk__in=final_route.bus_stops.all())
    mid_stop = common_stops[len(common_stops) - 1]
    multiple_routes = True if (common_stops.count() != start_route.bus_stops.count()) else False

    locations = []
    bus_stops = []

    routes = [start_route, final_route]
    start_cost = 0
    final_cost = 0
    cost = 0
    
    notify_stops = []
    notify_stops.append(start_route.bus_stops.all()[len(start_route.bus_stops.all()) - 1])
    if multiple_routes:
        start_stops = start_route.bus_stops.filter(
            stopinfo__weight=StopWeight.ROUTABLE
        ).all()
        stop = Stop.objects.get(lat=start_stop[0], lon=start_stop[1])
        s_stop_info = StopInfo.objects.get(route=start_route, stop=stop)
        if start_route.forward:
            start_bus_stops = \
                start_stops.filter(stopinfo__order__gte=s_stop_info.order).distinct()
        else:
            start_bus_stops = \
                reversed(
                    start_stops.filter(stopinfo__order__lte=s_stop_info.order).distinct()
                )

        count = StopInfo.objects.filter(route=start_route).count()
        start_cost = calculate_cost(start_route, s_stop_info, count)

        final_stops = final_route.bus_stops.filter(
            stopinfo__weight=StopWeight.ROUTABLE
        ).all()
        stop = Stop.objects.get(lat=final_stop[0], lon=final_stop[1])
        f_stop_info = StopInfo.objects.get(route=final_route, stop=stop)
        print(final_stops)
        if final_route.forward:
            final_bus_stops = \
                final_stops.filter(stopinfo__order__lte=f_stop_info.order).distinct()
        else:
            final_bus_stops = \
                reversed(
                    final_stops.filter(stopinfo__order__gte=f_stop_info.order).distinct())
        count = StopInfo.objects.filter(route=final_route).count()
        final_cost = calculate_cost(final_route, f_stop_info, count)

        cost = start_cost + final_cost

        bus_stops = []
        for s in start_bus_stops:
            bus_stops.append(s)

        locations.append([mid_stop.lat, mid_stop.lon])
        bus_stops.append(mid_stop)
        
        for s in final_bus_stops:
            bus_stops.append(s)

        print(bus_stops)

    else:
        mid_stop = None
        routes = [start_route]

        start_stops = start_route.bus_stops.filter(
            stopinfo__weight=StopWeight.ROUTABLE
        ).all()
        stop = Stop.objects.get(lat=start_stop[0], lon=start_stop[1])
        s_stop_info = StopInfo.objects.get(route=start_route, stop=stop)
        if start_route.forward:
            start_bus_stops = \
                start_stops.filter(stopinfo__order__gte=s_stop_info.order).distinct()
        else:
            start_bus_stops = \
                reversed(
                    start_stops.filter(stopinfo__order__lte=s_stop_info.order).distinct()
                )
        
        count = StopInfo.objects.filter(route=start_route).count()
        cost = calculate_cost(start_route, s_stop_info, count)

    print(locations)

    # journey = Journey
    start_stop_obj = Stop.objects.filter(lat=start_stop[0], lon=start_stop[1]).first()
    final_stop_obj = Stop.objects.filter(lat=final_stop[0], lon=final_stop[1]).first()

    # bus_stops.insert(0, start_stop_obj)
    # bus_stops.append(final_stop_obj)
    print("Routing Stops: ", bus_stops)

    journey = Journey.objects.create(
        from_location=from_loc,
        to_location=to_loc,
        start_stop=start_stop_obj,
        final_stop=final_stop_obj,
        mid_stop=mid_stop,
        start_cost=start_cost,
        final_cost=final_cost,
        cost=cost,
    )
    for s in notify_stops:
        journey.notify_stops.add(s)
    for r in routes:
        journey.routes.add(r)
    for s in bus_stops:
        journey.routing_stops.add(s)
    journey.save()
    serializer = JourneySerializer(Journey.objects.filter(id=journey.id).first())
    return JsonResponse(serializer.data, safe=True)

@csrf_exempt
def feedback(request):
    received_feedback = request.POST['feedback']
    user = request.POST['user']
    feedback = Feedback(user=user, feedback=received_feedback)
    feedback.save()
    return HttpResponse("Feedback added successfully!")

def calculate_cost(route:Route, stopInfo:StopInfo, count:int):
    cost = route.fee
    if route.fixed_fee:
        return cost

    count = StopInfo.objects.filter(route=route).count()
    if (cost >= 500) and route.forward:
        if (stopInfo.order / count) <= 0.75:
            cost = 0.6666 * cost
            cost = round(cost / 100)
            cost = cost * 100
    elif (cost >= 500) and (not route.forward):
        if (stopInfo.order / count) <= 1.333:
            cost =  0.666 * cost
            cost = round(cost / 100)
            cost = cost * 100

    return cost

        

def get_latest_journey(request):
    journey = Journey.objects.all().last()
    return JsonResponse(json.dumps(journey.directions), safe=False)

class GetRoute(generics.ListAPIView):
    serializer_class = JourneySerializer

    def get_queryset(self):
        if request.method != "GET":
            return HttpResponseNotAllowed("Methods other than GET not allowed")

        start_stop = (request.GET['start_lat'],request.GET['start_lon'])
        final_stop = (request.GET['final_lat'],request.GET['final_lon'])
        
        if (start_stop == None) or (final_stop == None):
            return HttpResponseBadRequest("Start and/or Final stops not set")

        overpassApi = overpy.Overpass()

        # fetch the real lat and lon
        start_stop, final_stop = getStartAndFinalStops(start_stop, overpassApi, final_stop)

        # find the origin route
        start_route = Route.objects.filter(bus_stops__lat=start_stop[0])
        start_route = start_route.filter(bus_stops__lon=start_stop[1]).first()

        # find the destination route
        final_route = Route.objects.filter(bus_stops__lat=final_stop[0])
        final_route = final_route.filter(bus_stops__lon=final_stop[1]).first()
        
        if (start_route == None) or (final_route == None):
            return Http404("Start/Final Stop not in any route")

        # the stops are in a route, calculate the waypoints
        common_stops = []
        mid_stop = None

        common_stops = start_route.bus_stops.filter(pk__in=final_route.bus_stops.all())
        mid_stop = common_stops[len(common_stops) - 1]
        multiple_routes = True if (common_stops.count() != start_route.bus_stops.count()) else False

        locations = []
        bus_stops = []

        routes = [start_route, final_route]
        cost = 0

        notify_stops = []
        notify_stops.append(start_route.bus_stops.all()[len(start_route.bus_stops.all()) - 2])
        if multiple_routes:
            cost = 1000
            for s in start_route.bus_stops.all():
                locations.append([s.lon, s.lat])
                bus_stops.append(s)
                print("Adding: ", s.name)
                if (s.lat == mid_stop.lat) and (s.lon == mid_stop.lon):
                    print("Broke at: ", s)
                    break
                
            # print(final_route.bus_stops.all())
            
            # final_route.bus_stops.reverse()
            final_stops = final_route.bus_stops.all()
            size = final_stops.count()
            print(size)
            for i in range(size - 1,0,-1):
                print("Adding: ", final_stops[i].name)
                # the mid stop has already been added
                if (final_stops[i].lat == mid_stop.lat) and (final_stops[i].lon == mid_stop.lon):
                    continue

                bus_stops.append(final_stops[i])
                locations.append([final_stops[i].lon, final_stops[i].lat])
                if (final_stops[i].lat == float(final_stop[0])) and (final_stops[i].lon == float(final_stop[1])):
                    notify_stops.append(final_stops[i+1])
                    print("Broke at: ", s)
                    break
        else:
            cost = 500
            routes = [final_route]
            for r in start_route.bus_stops.all():
                locations.append([r.lon, r.lat])
                if (r.lat == float(final_stop[0])) and (r.lon == float(final_stop[1])):
                    print("Broke at: ", r)
                    break

        print(locations)

        routing_client = ORS(
            api_key="5b3ce3597851110001cf62483a24528b22554895b20e36724d991206",
            retry_over_query_limit=False,
        )

        """ calculated_route = routing_client.directions(
            locations=locations,
            profile='driving-car',
            instructions=True,
            continue_straight=True
        ) """

        # journey = Journey
        start_stop_obj = Stop.objects.filter(lat=start_stop[0], lon=start_stop[1]).first()
        final_stop_obj = Stop.objects.filter(lat=final_stop[0], lon=final_stop[1]).first()

        journey = Journey(
            start_stop=start_stop_obj,
            final_stop=final_stop_obj,
            mid_stop=mid_stop,
            cost=cost
        )
        journey.save()

def getStartAndFinalStops(start_stop, overpassApi, final_stop):
    start_stop = (
        Decimal(start_stop[0]).normalize(), 
        Decimal(start_stop[1]).normalize())
    final_stop = (
        Decimal(final_stop[0]).normalize(), 
        Decimal(final_stop[1]).normalize())

    selectedStartStop = tuple()
    selectedFinalStop = tuple()

    earthCircumference = 40_030_173.59204115

    startDistance = earthCircumference
    finalDistance = earthCircumference

    stops = StopInfo.objects.all().distinct()
    stopLatAndLongs = []
    for s in stops:
        currentTuple = (float(s.stop.lat), float(s.stop.lon))
        calcStartDistance = haversine(
            start_stop, currentTuple, unit=Unit.METERS)
        calcFinalDistance = haversine(
            final_stop, currentTuple, unit=Unit.METERS)

        if calcStartDistance < startDistance:
            startDistance = calcStartDistance
            selectedStartStop = (s.stop.lat, s.stop.lon)

        if calcFinalDistance < finalDistance:
            finalDistance = calcFinalDistance
            selectedFinalStop = (s.stop.lat, s.stop.lon)


    return selectedStartStop, selectedFinalStop

def intersection(routeA, routeB):
    tupA = map(tuple, routeA)
    tupB = map(tuple, routeB)
    return list(map(list, set(tupA).intersection(tupB)))