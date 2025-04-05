from django.http import JsonResponse
import json
from external_modules.retriever_service import DataRetriever
from rest_framework.decorators import api_view
from rest_framework.response import Response

retriever = DataRetriever()

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

