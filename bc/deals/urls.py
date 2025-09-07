from django.urls import path
from .views import DealView, DropdownOptionView


urlpatterns = [
    path(
        "deals/", 
        DealView.as_view(), 
        name="deal"
    ),
    path(
        "dropdowns/", 
        DropdownOptionView.as_view(), 
        name="dropdown"
    ),
]