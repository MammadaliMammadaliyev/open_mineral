import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from deals.serializers import DropdownOptionSerializer
from deals.models import DropdownOption

logger = logging.getLogger("deals")


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
        logger.info(f"User {request.user} requested all dropdown options")
        dropdown_options = DropdownOption.objects.all()
        serializer = DropdownOptionSerializer(dropdown_options, many=True)
        logger.debug(f"Returned {len(serializer.data)} dropdown options")
        return Response(serializer.data, status=status.HTTP_200_OK)
