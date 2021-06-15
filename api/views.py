import csv, io, os, json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, Http404
from django.conf import settings
from rest_framework import viewsets

from .serializers import RouteSerializer, StopSerializer
from .models import Route, Stop

from routingpy import ORS, Graphhopper

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

def get_route(request):
    if request.method != "GET":
        return HttpResponseNotAllowed("Methods other than GET not allowed")

    start_stop = (request.GET['start_lat'],request.GET['start_lon'])
    final_stop = (request.GET['final_lat'],request.GET['final_lon'])
    
    if (start_stop == None) or (final_stop == None):
        return HttpResponseBadRequest("Start and/or Final stops not set")

    print("start_stop =",start_stop[0],"final_stop =",final_stop)

    # find the origin route
    start_route = Route.objects.filter(bus_stops__lat=start_stop[0])
    start_route = start_route.filter(bus_stops__lon=start_stop[1]).first()

    # find the destination route
    final_route = Route.objects.filter(bus_stops__lat=final_stop[0])
    final_route = final_route.filter(bus_stops__lon=final_stop[1]).first()
    
    if (start_route == None) or (final_route == None):
        return Http404("Start/Final Stop not in any route")

    # the stops are in a route, calculate the waypoints
    route = []
    # if final_route == start_route:
    route = final_route

    locations = []
    for r in route.bus_stops.all():
        locations.append([r.lon, r.lat])
        if (r.lat == float(final_stop[0])) and (r.lon == float(final_stop[1])):
            print("Broke at: ", r)
            break

    print(route.bus_stops.all())
    print(locations)

    routing_client = ORS(
        api_key="5b3ce3597851110001cf62483a24528b22554895b20e36724d991206",
        retry_over_query_limit=False,
    )

    calculated_route = routing_client.directions(
        locations=locations,
        profile='driving-car',
        instructions=True,
        continue_straight=True
    )

    
    return HttpResponse(json.dumps(calculated_route.__dict__))
