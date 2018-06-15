from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('polygon/batch-upload', views.upload_polygons, name='upload_polygons'),
    path('polygon', views.get_polygons, name='get_polygons'),
]