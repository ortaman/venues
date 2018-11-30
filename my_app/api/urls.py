
from django.urls import path
from .views import FourSquareVenuesAPIView


urlpatterns = [
    path('venues/', FourSquareVenuesAPIView.as_view()),
]
