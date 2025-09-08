import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from deals.services.ai_suggestions import ai_suggestions_service
from deals.response_messages import ResponseMessages

logger = logging.getLogger("deals")


class AISuggestionsView(APIView):
    """
    Simple API endpoint that provides AI suggestions for commercial terms fields
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get AI suggestion for a specific field",
        manual_parameters=[
            openapi.Parameter(
                'field_name',
                openapi.IN_QUERY,
                description="Name of the field to get suggestions for",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'field_value',
                openapi.IN_QUERY,
                description="Current value of the field",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="AI suggestion response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['info', 'warning', 'error']),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'suggested_value': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL),
                        'show_accept_button': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request - Missing required parameters",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def get(self, request):
        """
        Get AI suggestion for a specific field
        
        Query Parameters:
        - field_name: Name of the field (e.g., 'prepayment', 'treatment_charge', 'refining_charge')
        - field_value: Current value of the field
        """
        field_name = request.query_params.get('field_name')
        field_value = request.query_params.get('field_value')
        logger.info(f"User {request.user} requested AI suggestion for field {field_name} with value {field_value}")
        
        if not field_name or field_value is None:
            return Response(
                {'error': ResponseMessages.MISSING_REQUIRED_PARAMETERS},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"Getting AI suggestion for field {field_name} with value {field_value}")
        suggestion = ai_suggestions_service.get_suggestion(
            field_name=field_name,
            field_value=field_value
        )

        if suggestion:
            logger.info(f"AI suggestion for field {field_name} with value {field_value} found")
            return Response(suggestion, status=status.HTTP_200_OK)
        else:
            logger.info(f"No AI suggestion found for field {field_name} with value {field_value}")
            return Response(
                {'message': ResponseMessages.NO_SUGGESTIONS_AVAILABLE},
                status=status.HTTP_200_OK
            )
