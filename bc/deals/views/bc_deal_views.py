from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from deals.serializers import BusinessConfirmationDealSerializer
from deals.models import BusinessConfirmationDeal


class BusinessConfirmationDealView(APIView):
    """
    API endpoint that allows business confirmation deals to be viewed or created.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all business confirmation deals",
        responses={200: BusinessConfirmationDealSerializer(many=True)}
    )
    def get(self, request):
        business_confirmation_deals = BusinessConfirmationDeal.objects.all()
        serializer = BusinessConfirmationDealSerializer(business_confirmation_deals, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new business confirmation deal",
        request_body=BusinessConfirmationDealSerializer,
        responses={201: BusinessConfirmationDealSerializer}
    )
    def post(self, request):
        serializer = BusinessConfirmationDealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)