import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from deals.serializers import CommercialTermsSerializer, AdditionalClauseSerializer
from deals.models import AdditionalClause, CommercialTerms

logger = logging.getLogger("deals")


class CommercialTermsView(APIView):
    """
    API endpoint that allows commercial terms to be viewed or created.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all commercial terms",
        responses={200: CommercialTermsSerializer(many=True)}
    )
    def get(self, request):
        logger.info(f"User {request.user} requested all commercial terms")
        commercial_terms = CommercialTerms.objects.all()
        serializer = CommercialTermsSerializer(commercial_terms, many=True)
        logger.debug(f"Returned {len(serializer.data)} commercial terms")
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new commercial terms",
        request_body=CommercialTermsSerializer,
        responses={201: CommercialTermsSerializer}
    )
    def post(self, request):
        logger.info(f"User {request.user} is creating a commercial terms")
        serializer = CommercialTermsSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logger.info(f"CommercialTerms {instance.id} created by {request.user}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to create CommercialTerms by {request.user}. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdditionalClauseView(APIView):
    """
    API endpoint that allows additional clauses to be viewed
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all additional clauses",
        responses={200: AdditionalClauseSerializer(many=True)}
    )
    def get(self, request):
        logger.info(f"User {request.user} requested all additional clauses")
        additional_clauses = AdditionalClause.objects.all()
        serializer = AdditionalClauseSerializer(additional_clauses, many=True)
        logger.debug(f"Returned {len(serializer.data)} additional clauses")
        return Response(serializer.data)