from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from deals.serializers import DropdownOptionSerializer
from deals.models import DropdownOption


class DropdownOptionView(APIView):
    """
    API endpoint that allows dropdown options to be viewed or created.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all dropdown options",
        responses={200: DropdownOptionSerializer(many=True)}
    )
    def get(self, request):
        dropdown_options = DropdownOption.objects.all()
        serializer = DropdownOptionSerializer(dropdown_options, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
