from rest_framework import serializers
from .models import Route, Stop, Journey

class StopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stop
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'
        depth = 2

class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = '__all__'
        depth = 1