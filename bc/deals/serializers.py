from rest_framework import serializers
from .models import BusinessConfirmationDeal, DropdownOption


class BusinessConfirmationDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessConfirmationDeal
        fields = "__all__"


class DropdownOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropdownOption
        fields = "__all__"