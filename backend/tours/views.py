from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import filter_tours
from .models import Tour
from .serializers import TourSerializer


class TourListView(APIView):
    """GET /api/tours/ — список с query-параметрами как на фронте."""

    def get(self, request):
        params = request.GET.dict()
        filtered = filter_tours(Tour.objects.all(), params)
        return Response(TourSerializer(filtered, many=True).data)


class TourDetailView(APIView):
    """GET /api/tours/<slug>/"""

    def get(self, request, slug: str):
        try:
            tour = Tour.objects.get(slug=slug)
        except Tour.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(TourSerializer(tour).data)
