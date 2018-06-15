from django.http import JsonResponse
from django.shortcuts import render
from elasticsearch import Elasticsearch

import os, json

def index(request):
    context = {}
    return render(request, 'geofencing/index.html', context)

def get_polygons(request):
    polygons_file = open(os.path.dirname(os.path.realpath(__file__)) + '/data/polygons.json')
    response = json.loads(polygons_file.read())
    polygons_file.close()
    return JsonResponse(response, safe=False)

def upload_polygons(request):
    polygons_file = open(os.path.dirname(os.path.realpath(__file__)) + '/data/polygons.json')
    polygons = json.loads(polygons_file.read())
    polygons_file.close()

    es = Elasticsearch(
        ['elasticsearch'],
        port=9200,
    )

    place = {
        "location" : {
            "type" : "polygon",
            "coordinates": [
                [
                    [-75.575060,6.202118],
                    [-75.577248,6.202865],
                    [-75.579437,6.194759],
                    [-75.576326,6.193116],
                    [-75.574545,6.191687],
                    [-75.572141,6.192113],
                    [-75.571154,6.194908],
                    [-75.569524,6.197404],
                    [-75.575060,6.202118]
                ]
            ]
        }
    }

    res = es.index(index="bateshotel", doc_type='places', id=1, body=place)
    print(res['result'])
    return JsonResponse(res)


############# GEO SHAPE QUERY #############
# {
#     "query":{
#         "bool": {
#             "must": {
#                 "match_all": {}
#             },
#             "filter": {
#                 "geo_shape": {
#                     "location": {
#                         "shape": {
#                             "type": "point",
#                             "coordinates" : [-75.5739779, 6.1964829]
#                         },
#                         "relation": "contains"
#                     }
#                 }
#             }
#         }
#     }
# }