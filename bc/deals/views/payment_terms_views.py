import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from deals.serializers import PaymentTermsSerializer
from drf_yasg.utils import swagger_auto_schema
from deals.models import PaymentTerms

logger = logging.getLogger("deals")


class PaymentTermsView(APIView):
    """
    API endpoint that allows payment terms to be viewed or created.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all payment terms",
        responses={200: PaymentTermsSerializer(many=True)}
    )
    def get(self, request):
        logger.info(f"User {request.user} requested all payment terms")
        payment_terms = PaymentTerms.objects.all()
        serializer = PaymentTermsSerializer(payment_terms, many=True)
        logger.debug(f"Returned {len(serializer.data)} payment terms")
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new payment terms",
        request_body=PaymentTermsSerializer,
        responses={201: PaymentTermsSerializer}
    )
    def post(self, request):
        logger.info(f"User {request.user} is creating a payment terms")
        serializer = PaymentTermsSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logger.info(f"PaymentTerms {instance.id} created by {request.user}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to create PaymentTerms by {request.user}. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
