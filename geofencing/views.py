from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from elasticsearch import Elasticsearch

import os, json

def index(request):
    context = {}
    coordinates = request.GET.get("coordinates", None)
    context["coordinates"] = coordinates
    return render(request, 'geofencing/index.html', context)

def upload_polygons(request):
    polygons_file = open(os.path.dirname(os.path.realpath(__file__)) + '/data/polygons.json')
    polygons = json.loads(polygons_file.read())
    polygons_file.close()

    es = Elasticsearch(
        ['elasticsearch'],
        port=9200,
    )
    place = {
        "name": "",
        "active": True,
        "location" : {
            "type" : "polygon",
            "coordinates": []
        }
    }

    results = []
    for polygon in polygons:
        place["name"] = polygon["name"]
        place["location"]["coordinates"] = polygon["coordinates"]
        res = es.index(index="bateshotel", doc_type="places", body=place)
        results.append(res)

    return JsonResponse(results, safe=False)

def search_places(request):
    es = Elasticsearch(
        ['elasticsearch'],
        port=9200,
    )

    query = {
        "query":{
            "bool": {
                "must": {
                    "match_all": {}
                }
            }
        }
    }

    coordinates = request.GET.get("coordinates", None)
    if coordinates and coordinates != "None":
        latitude, longitude = coordinates.split(",")
        query["query"]["bool"]["filter"] = {
            "geo_shape": {
                "location": {
                    "shape": {
                        "type": "point",
                        "coordinates" : [longitude, latitude]
                    },
                    "relation": "contains"
                }
            }
        }

    response = []
    res = es.search(index="bateshotel", doc_type="places", body=query)
    for hit in res['hits']['hits']:
        response.append(hit["_source"])

    return JsonResponse(response, safe=False)
