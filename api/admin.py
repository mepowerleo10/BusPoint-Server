from django.contrib import admin
from django.forms import ModelForm
from .models import Route, Stop, StopInfo

# Register your models here.

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    search_fields = ['name', 'start_point__name', 'end_point__name']
    fields = ('name', 'start_point', 'end_point', 'first_stripe', 'last_stripe')
    ordering = ['start_point', 'end_point']


class StopInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StopInfoForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['stop'].queryset = Stop.objects.all().order_by('name')
    
    class Meta:
        model = StopInfo
        fields = '__all__'

@admin.register(StopInfo)
class StopInfoAdmin(admin.ModelAdmin):
    form = StopInfoForm
    search_fields = ['stop__name', 'route__name']

@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    search_fields = ['name', 'lat', 'lon']

# admin.site.register(Route)
# admin.site.register(Stop)
# admin.site.register(StopInfo)
