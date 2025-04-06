from django.http import JsonResponse
import json
from external_modules.retriever_service import DataRetriever
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

retriever = DataRetriever()
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            name='strategy_type', 
            in_=openapi.IN_QUERY, 
            description="Type of strategy (e.g., 'wfs', 'wms', )", 
            type=openapi.TYPE_STRING,
            default='wfs'
        ),
        openapi.Parameter(
            name='url', 
            in_=openapi.IN_QUERY, 
            description="URL from external source", 
            type=openapi.TYPE_STRING,
            default='https://mapas2.igac.gov.co/server/rest/services/geodesia/redgravimetrica/MapServer'
        ),
        openapi.Parameter(
            name='polygon', 
            in_=openapi.IN_QUERY, 
            description="List of coordinates as a JSON string (e.g., '[[lon1, lat1], [lon2, lat2]],...')", 
            type=openapi.TYPE_STRING,
            default='[[-74.12, 4.65],[-74.16, 4.68],[-74.10, 4.70]]'
        ),
        openapi.Parameter(
            name='CRS', 
            in_=openapi.IN_QUERY, 
            description="Coordinate Reference System (e.g., 'EPSG:4326')", 
            type=openapi.TYPE_STRING,
            default='EPSG:4326'
        ),
    ],
    responses={200: "Success", 400: "Bad Request"}
)
@api_view(['GET'])
def get_data(request):
    strategy_type = request.query_params['strategy_type']
    url = request.query_params['url']
    polygon = request.query_params['polygon']
    CRS = request.query_params['CRS']
    try:
        if not polygon:
            return JsonResponse({"error": "Polygon parameter is required"}, status=400)
        polygon_list = json.loads(polygon)
        polygon = [tuple(coord) for coord in polygon_list]
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid polygon format"}, status=400)

    data = retriever.get_data(
        strategy_type=strategy_type,
        url=url,
        polygon=polygon,
        CRS=CRS
    )

    return JsonResponse(data, safe=False)

