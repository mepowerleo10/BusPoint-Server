from django.contrib import admin
from .models import Route, Stop, StopInfo

# Register your models here.
admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(StopInfo)
