from django.urls import path
from .views import (NewBusinessConfirmationView, DropdownOptionView, CommercialTermsView, 
                    AdditionalClauseView, PaymentTermsView, BusinessConfirmationDealView,
                    AISuggestionsView)


app_name = "deals"

urlpatterns = [
    path(
        "new-business-confirmations/", 
        NewBusinessConfirmationView.as_view(), 
        name="new-business-confirmation"
    ),
    path(
        "dropdowns/", 
        DropdownOptionView.as_view(), 
        name="dropdown"
    ),
    path(
        "commercial-terms/", 
        CommercialTermsView.as_view(), 
        name="commercial-terms"
    ),
    path(
        "additional-clauses/", 
        AdditionalClauseView.as_view(), 
        name="additional-clauses"
    ),
    path(
        "payment-terms/", 
        PaymentTermsView.as_view(), 
        name="payment-terms"
    ),
    path(
        "business-confirmation-deals/", 
        BusinessConfirmationDealView.as_view(), 
        name="business-confirmation-deals"
    ),
    path(
        "ai-suggestions/", 
        AISuggestionsView.as_view(), 
        name="ai-suggestions"
    )
]
