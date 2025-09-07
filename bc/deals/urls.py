from django.urls import path
from .views import BusinessConfirmationDealView, DropdownOptionView


urlpatterns = [
    path(
        "business-confirmation-deals/", 
        BusinessConfirmationDealView.as_view(), 
        name="business-confirmation-deal"
    ),
    path(
        "dropdowns/", 
        DropdownOptionView.as_view(), 
        name="dropdown"
    ),
]