from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .serializers import DealSerializer


class DealView(APIView):
    """
    API endpoint that allows deals to be viewed or created.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all deals",
        responses={200: DealSerializer(many=True)}
    )
    def get(self, request):
        return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new deal",
        request_body=DealSerializer,
        responses={201: DealSerializer}
    )
    def post(self, request):
        return Response({"message": "Hello, world!"}, status=status.HTTP_201_CREATED)