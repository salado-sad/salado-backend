from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, CartViewSet

router = DefaultRouter()
router.register(r'items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    path('', CartViewSet.as_view({'get': 'list'}), name='cart'),
    path('', include(router.urls)),
]
