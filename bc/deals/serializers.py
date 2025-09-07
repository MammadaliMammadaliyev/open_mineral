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
