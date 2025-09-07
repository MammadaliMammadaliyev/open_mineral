from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from deals.serializers import CommercialTermsSerializer, AdditionalClauseSerializer
from deals.models import AdditionalClause, CommercialTerms


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
        commercial_terms = CommercialTerms.objects.all()
        serializer = CommercialTermsSerializer(commercial_terms, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new commercial terms",
        request_body=CommercialTermsSerializer,
        responses={201: CommercialTermsSerializer}
    )
    def post(self, request):
        serializer = CommercialTermsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        additional_clauses = AdditionalClause.objects.all()
        serializer = AdditionalClauseSerializer(additional_clauses, many=True)
        return Response(serializer.data)