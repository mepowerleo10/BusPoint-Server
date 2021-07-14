from django.db import models
import datetime
from .enums import RouteColors
from sortedm2m.fields import SortedManyToManyField

# Create your models here.
class Stop(models.Model):
    name = models.CharField(max_length=80)
    lat = models.CharField(max_length=11)
    lon = models.CharField(max_length=11)

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=80)
    start_point = models.ForeignKey(Stop, on_delete=models.CASCADE, 
        related_name="start_point")
    end_point = models.ForeignKey(Stop, on_delete=models.CASCADE, 
        related_name="end_point")
    forward = models.BooleanField(default=True)
    bus_stops = models.ManyToManyField(Stop, through='StopInfo' ,
        related_name="bus_stops")
    first_stripe = models.CharField(choices=RouteColors.choices(), 
        default=RouteColors.WHITE, max_length=9)
    last_stripe = models.CharField(choices=RouteColors.choices(),
        default=RouteColors.WHITE, max_length=9)

    def __str__(self):
        return self.name
        
    """ def __eq__(self, other):
        if other != None:
            return self.__dict__ == other.__dict__ """

class StopWeight(models.IntegerChoices):
    NORMAL = 1, 'Normal'
    ROUTABLE = 2, 'Routable'

class StopInfo(models.Model):
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    weight = models.IntegerField(choices=StopWeight.choices,
        default=StopWeight.NORMAL)

class Journey(models.Model):
    """ def __init__(self, start_stop, final_stop, mid_stop, notify_stops, routes, cost):
        self.start_stop = start_stop
        self.final_stop = final_stop
        self.mid_stop = mid_stop
        self.notify_stops = notify_stops
        self.routes = routes
        self.cost = cost """
    date = models.DateTimeField(auto_now_add=True, blank=True)
    # location_name = models.CharField(max_length=50)
    # destination_name = models.CharField(max_length=50)
    start_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, 
        related_name="start_stop")
    final_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, 
        related_name="final_stop")
    mid_stop = models.ForeignKey(Stop, null=True, on_delete=models.CASCADE, 
        related_name="mid_stop")
    notify_stops = SortedManyToManyField(Stop, related_name="notify_stops")
    routing_stops = SortedManyToManyField(Stop, related_name="routing_stops")
    routes = SortedManyToManyField(Route, related_name="routes")
    cost = models.FloatField(max_length=5)