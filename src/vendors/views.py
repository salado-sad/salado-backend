from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Product
from .serializers import ProductSerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def all_products(self, request):
        """Retrieve all products, regardless of owner."""
        products = Product.objects.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
