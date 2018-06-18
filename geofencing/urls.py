from django.urls import path

from . import views

urlpatterns = [
    path('/list', views.index, name='index'),
    path('/polygon/batch-upload', views.upload_polygons, name='upload_polygons'),
    path('/api/search-places', views.search_places, name='search_places'),
]