from rest_framework import serializers
from .models import Route, Stop

class StopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stop
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'
        depth = 2
