import csv, io, os
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets

from .serializers import RouteSerializer, StopSerializer
from .models import Route, Stop

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
