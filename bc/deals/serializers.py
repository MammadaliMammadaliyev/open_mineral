from rest_framework import serializers
from .models import (NewBusinessConfirmation, DropdownOption, 
                     CommercialTerms, BusinessConfirmationDeal,
                     AdditionalClause)


class NewBusinessConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewBusinessConfirmation
        fields = "__all__"


class DropdownOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropdownOption
        fields = "__all__"


class CommercialTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialTerms
        fields = "__all__"


class AdditionalClauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalClause
        fields = "__all__"


class BusinessConfirmationDealSerializer(serializers.ModelSerializer):
    new_business_confirmation = NewBusinessConfirmationSerializer()
    commercial_terms = CommercialTermsSerializer()

    class Meta:
        model = BusinessConfirmationDeal
        fields = "__all__"