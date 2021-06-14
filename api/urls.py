from django.urls import include, path
from rest_framework import routers
from . import views
from .views import upload_stops

router = routers.DefaultRouter()
router.register(r'Routes', views.RouteViewSet)
router.register(r'Stops', views.StopViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('upload-stops/', upload_stops, name="upload_stops"),
    path('api-auth/', include('rest_framework.urls', 
        namespace='rest_framework'))
]
