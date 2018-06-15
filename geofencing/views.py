from django.http import JsonResponse
from django.shortcuts import render
import os, json

def index(request):
    context = {}
    return render(request, 'geofencing/index.html', context)

def get_polygons(request):
    polygons_file = open(os.path.dirname(os.path.realpath(__file__)) + '/data/polygons.json')
    response = json.loads(polygons_file.read())
    polygons_file.close()
    return JsonResponse(response, safe=False)