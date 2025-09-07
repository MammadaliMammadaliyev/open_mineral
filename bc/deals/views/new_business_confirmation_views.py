from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from deals.serializers import NewBusinessConfirmationSerializer
from deals.models import NewBusinessConfirmation


class NewBusinessConfirmationView(APIView):
    """
    API endpoint that allows deals to be viewed or created.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all deals",
        responses={200: NewBusinessConfirmationSerializer(many=True)}
    )
    def get(self, request):
        deals = NewBusinessConfirmation.objects.all()
        serializer = NewBusinessConfirmationSerializer(deals, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new deal",
        request_body=NewBusinessConfirmationSerializer,
        responses={201: NewBusinessConfirmationSerializer}
    )
    def post(self, request):
        serializer = NewBusinessConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)