from rest_framework import serializers
from .models import (NewBusinessConfirmation, DropdownOption, 
                     CommercialTerms, BusinessConfirmationDeal,
                     AdditionalClause, PaymentTerms)


class NewBusinessConfirmationSerializer(serializers.ModelSerializer):
    """
    Serializer for New Business Confirmation
    """
    class Meta:
        model = NewBusinessConfirmation
        fields = "__all__"


class DropdownOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Dropdown Option
    """
    class Meta:
        model = DropdownOption
        fields = "__all__"


class CommercialTermsSerializer(serializers.ModelSerializer):
    """
    Serializer for Commercial Terms
    """
    class Meta:
        model = CommercialTerms
        fields = "__all__"


class AdditionalClauseSerializer(serializers.ModelSerializer):
    """
    Serializer for Additional Clause
    """
    class Meta:
        model = AdditionalClause
        fields = ("clause",)


class PaymentTermsSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment Terms
    """
    class Meta:
        model = PaymentTerms
        fields = "__all__"


class BusinessConfirmationDealSerializer(serializers.ModelSerializer):
    """
    Serializer for Business Confirmation Deal
    """
    class Meta:
        model = BusinessConfirmationDeal
        fields = "__all__"


class AISuggestionSerializer(serializers.Serializer):
    """
    Serializer for AI suggestion responses
    """
    type = serializers.ChoiceField(choices=['info', 'warning', 'error'])
    message = serializers.CharField(max_length=500)
    suggested_value = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True, required=False)
    show_accept_button = serializers.BooleanField(default=False)
    suggested_options = serializers.ListField(
        child=serializers.CharField(max_length=100),
        allow_null=True,
        required=False
    )
    warning_type = serializers.CharField(max_length=50, allow_null=True, required=False)
