
from django.urls import path
from .views import FourSquareVenuesAPIView, FavoriteViewSet


urlpatterns = [
    path('venues/', FourSquareVenuesAPIView.as_view()),
    path('favorite/', FavoriteViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('favorite/<int:pk>/', FavoriteViewSet.as_view({'patch': 'partial_update', 'delete':'destroy'})),
]
