from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('geofencing', include('geofencing.urls')),
    path('admin/', admin.site.urls),
]
