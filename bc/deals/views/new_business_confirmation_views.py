import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from deals.serializers import NewBusinessConfirmationSerializer
from deals.models import NewBusinessConfirmation

logger = logging.getLogger("deals")


class NewBusinessConfirmationView(APIView):
    """
    API endpoint that allows new business confirmations to be viewed or created.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all new business confirmations",
        responses={200: NewBusinessConfirmationSerializer(many=True)}
    )
    def get(self, request):
        logger.info(f"User {request.user} requested all new business confirmations")
        new_business_confirmations = NewBusinessConfirmation.objects.all()
        serializer = NewBusinessConfirmationSerializer(new_business_confirmations, many=True)
        logger.debug(f"Returned {len(serializer.data)} new business confirmations")
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new new business confirmation",
        request_body=NewBusinessConfirmationSerializer,
        responses={201: NewBusinessConfirmationSerializer}
    )
    def post(self, request):
        logger.info(f"User {request.user} is creating a new business confirmation")
        serializer = NewBusinessConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logger.info(f"NewBusinessConfirmation {instance.id} created by {request.user}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to create NewBusinessConfirmation by {request.user}. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)