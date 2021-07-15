from django.contrib import admin
from django.forms import ModelForm
from .models import Route, Stop, StopInfo, Journey, Feedback

# Register your models here.

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    search_fields = ['name', 'start_point__name', 'end_point__name']
    fields = ('name', 'start_point', 'end_point', 'first_stripe', 'last_stripe', 'forward')
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
    search_fields = ['stop__name', 'route__name', 'weight']
    list_display = ('stop', 'route', 'weight')
    list_filter = ['weight', 'route']

@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    search_fields = ['name', 'lat', 'lon']
    list_display = ('name', 'lat', 'lon')

@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    search_fields = ['routes']
    list_display = ('__str__', 'start_stop', 'final_stop', 'mid_stop', 'cost')
    list_filter = ('routes',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    search_fields = ['feedback', 'user', 'checked', 'date']
    list_display = ('date', 'feedback', 'user', 'checked')
    list_filter = ('checked', 'date')

# admin.site.register(Route)
# admin.site.register(Stop)
# admin.site.register(StopInfo)

# admin.site.register(Journey)