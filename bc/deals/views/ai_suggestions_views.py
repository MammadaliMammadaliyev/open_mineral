from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from deals.serializers import AISuggestionSerializer
from deals.services.ai_suggestions import ai_suggestions_service


class AISuggestionsView(APIView):
    """
    API endpoint that provides AI suggestions for commercial terms fields
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get AI suggestions for a specific field",
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
            ),
            openapi.Parameter(
                'material',
                openapi.IN_QUERY,
                description="Material type for context (optional)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'transport_mode',
                openapi.IN_QUERY,
                description="Transport mode for context (optional)",
                type=openapi.TYPE_STRING,
                required=False
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
                        'show_accept_button': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'suggested_options': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        ),
                        'warning_type': openapi.Schema(type=openapi.TYPE_STRING)
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
        - field_name: Name of the field (e.g., 'treatment_charge', 'refining_charge', 'packaging')
        - field_value: Current value entered by user
        - material: Material type for context (optional)
        - transport_mode: Transport mode for context (optional)
        """
        field_name = request.query_params.get('field_name')
        field_value = request.query_params.get('field_value')
        material = request.query_params.get('material')
        transport_mode = request.query_params.get('transport_mode')
        
        if not field_name or field_value is None:
            return Response(
                {'error': 'field_name and field_value are required parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert field_value to appropriate type
        try:
            # Try to convert to float for numeric fields
            if field_name in ['treatment_charge', 'refining_charge']:
                field_value = float(field_value)
        except (ValueError, TypeError):
            # Keep as string if conversion fails
            pass
        
        # Get suggestion from AI service
        suggestion = ai_suggestions_service.get_suggestion(
            field_name=field_name,
            field_value=field_value,
            material=material,
            transport_mode=transport_mode
        )
        
        # If no specific suggestion, try general suggestions
        if not suggestion:
            context = {
                'material': material,
                'transport_mode': transport_mode
            }
            suggestion = ai_suggestions_service.get_general_suggestion(
                field_name=field_name,
                field_value=field_value,
                context=context
            )
        
        if suggestion:
            serializer = AISuggestionSerializer(suggestion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'No suggestions available for this field'},
                status=status.HTTP_200_OK
            )


class AISuggestionsBatchView(APIView):
    """
    API endpoint that provides AI suggestions for multiple fields at once
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get AI suggestions for multiple fields",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'fields': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'field_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'field_value': openapi.Schema(type=openapi.TYPE_STRING),
                            'material': openapi.Schema(type=openapi.TYPE_STRING),
                            'transport_mode': openapi.Schema(type=openapi.TYPE_STRING)
                        },
                        required=['field_name', 'field_value']
                    )
                )
            },
            required=['fields']
        ),
        responses={
            200: openapi.Response(
                description="Batch AI suggestions response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'suggestions': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['info', 'warning', 'error']),
                                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                                    'suggested_value': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL),
                                    'show_accept_button': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'suggested_options': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(type=openapi.TYPE_STRING)
                                    ),
                                    'warning_type': openapi.Schema(type=openapi.TYPE_STRING),
                                    'field_name': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request - Invalid input data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def post(self, request):
        """
        Get AI suggestions for multiple fields
        
        Request Body:
        {
            "fields": [
                {
                    "field_name": "treatment_charge",
                    "field_value": "320.00",
                    "material": "Lead Concentrate"
                },
                {
                    "field_name": "refining_charge", 
                    "field_value": "5.00",
                    "material": "Lead Concentrate"
                }
            ]
        }
        """
        fields = request.data.get('fields', [])
        
        if not fields or not isinstance(fields, list):
            return Response(
                {'error': 'fields array is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        suggestions = []
        
        for field_data in fields:
            field_name = field_data.get('field_name')
            field_value = field_data.get('field_value')
            material = field_data.get('material')
            transport_mode = field_data.get('transport_mode')
            
            if not field_name or field_value is None:
                continue
            
            # Convert field_value to appropriate type
            try:
                if field_name in ['treatment_charge', 'refining_charge']:
                    field_value = float(field_value)
            except (ValueError, TypeError):
                pass
            
            # Get suggestion
            suggestion = ai_suggestions_service.get_suggestion(
                field_name=field_name,
                field_value=field_value,
                material=material,
                transport_mode=transport_mode
            )
            
            if suggestion:
                suggestion['field_name'] = field_name
                suggestions.append(suggestion)
        
        return Response(
            {'suggestions': suggestions},
            status=status.HTTP_200_OK
        )
