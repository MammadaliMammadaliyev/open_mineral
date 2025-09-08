import logging
from django.core.cache import cache
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
    Implements intelligent caching that invalidates when data changes.
    """
    permission_classes = [IsAuthenticated]
    
    CACHE_KEY = "dropdown_options_all"
    CACHE_TIMEOUT = 3600
    
    @swagger_auto_schema(
        operation_description="Get all dropdown options (cached)",
        responses={200: DropdownOptionSerializer(many=True)}
    )
    def get(self, request):
        logger.info(f"User {request.user} requested all dropdown options")

        cached_data = cache.get(self.CACHE_KEY)

        if cached_data is not None:
            logger.debug("Returning dropdown options from cache")
            return Response(cached_data, status=status.HTTP_200_OK)

        logger.debug("Cache miss - fetching dropdown options from database")
        dropdown_options = DropdownOption.objects.filter(is_active=True).order_by('field_name', 'display_order')
        serializer = DropdownOptionSerializer(dropdown_options, many=True)

        cache.set(self.CACHE_KEY, serializer.data, self.CACHE_TIMEOUT)

        logger.debug(f"Returned {len(serializer.data)} dropdown options and cached them")
        return Response(serializer.data, status=status.HTTP_200_OK)
