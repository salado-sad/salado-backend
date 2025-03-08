from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, AllProductsView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('all-products/', AllProductsView.as_view(), name='all-products'),
]
