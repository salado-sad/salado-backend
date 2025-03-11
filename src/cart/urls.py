# cart/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, CartViewSet, PurchaseListView, PublicCartItemViewSet

router = DefaultRouter()
router.register(r'items', CartItemViewSet, basename='cartitem')
router.register(r'public/items', PublicCartItemViewSet, basename='public-cartitem')  # Public endpoint

urlpatterns = [
    path('', CartViewSet.as_view({'get': 'list'}), name='cart'),
    path('purchases/', PurchaseListView.as_view(), name='purchases'),
    path('', include(router.urls)),
]
