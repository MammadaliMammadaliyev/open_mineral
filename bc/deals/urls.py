from django.urls import path
from .views import DealView


urlpatterns = [
    path(
        "deals/", 
        DealView.as_view(), 
        name="deal"
    ),
]