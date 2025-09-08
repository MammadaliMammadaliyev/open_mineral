import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from deals.serializers import BusinessConfirmationDealSerializer
from deals.models import BusinessConfirmationDeal
from rest_framework.throttling import UserRateThrottle

logger = logging.getLogger("deals")


class BusinessConfirmationDealView(APIView):
    """
    API endpoint that allows business confirmation deals to be viewed or created.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @swagger_auto_schema(
        operation_description="Get all business confirmation deals",
        responses={200: BusinessConfirmationDealSerializer(many=True)}
    )
    def get(self, request):
        logger.info(f"User {request.user} requested all business confirmation deals")
        business_confirmation_deals = BusinessConfirmationDeal.objects.all()
        serializer = BusinessConfirmationDealSerializer(business_confirmation_deals, many=True)
        logger.debug(f"Returned {len(serializer.data)} deals")
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new business confirmation deal",
        request_body=BusinessConfirmationDealSerializer,
        responses={201: BusinessConfirmationDealSerializer}
    )
    def post(self, request):
        logger.info(f"User {request.user} is creating a business confirmation deal")
        serializer = BusinessConfirmationDealSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logger.info(f"BusinessConfirmationDeal {instance.id} created by {request.user}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Failed to create BusinessConfirmationDeal by {request.user}. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)