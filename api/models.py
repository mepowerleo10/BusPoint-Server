from django.db import models
from .enums import RouteColors

# Create your models here.
class Stop(models.Model):
    name = models.CharField(max_length=80)
    lat = models.FloatField(max_length=8)
    lon = models.FloatField(max_length=8)

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=80)
    start_point = models.OneToOneField(Stop, on_delete=models.CASCADE, related_name="start_point")
    end_point = models.OneToOneField(Stop, on_delete=models.CASCADE, related_name="end_point")
    forward = models.BooleanField(default=True)
    bus_stops = models.ManyToManyField(Stop, through='StopInfo' ,related_name="bus_stops")
    first_stripe = models.CharField(choices=RouteColors.choices(), default=RouteColors.WHITE, max_length=9)
    last_stripe = models.CharField(choices=RouteColors.choices(), default=RouteColors.WHITE, max_length=9)

    def __str__(self):
        return self.name
        
    def __eq__(self, other):
        if other != None:
            return self.__dict__ == other.__dict__

class StopInfo(models.Model):
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()