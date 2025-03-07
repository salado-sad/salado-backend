# cart/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.exceptions import PermissionDenied, ValidationError

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get or create the current user's cart items
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        return CartItem.objects.filter(cart=cart)
    
    def perform_create(self, serializer):
        user = self.request.user
        # ✅ CHECK 1: Ensure only customers can add to cart
        if not user.groups.filter(name="customer").exists():
            raise PermissionDenied("Only customers can add to cart.")
        
        cart, _ = Cart.objects.get_or_create(user=user)
        package = serializer.validated_data["package"]
        quantity = serializer.validated_data.get("quantity", 1)
        
        # ✅ CHECK 2: Ensure cart quantity doesn't exceed package stock
        if quantity > package.stock_quantity:
            raise ValidationError("Not enough stock available for this package.")
        
        # Check if the package already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, package=package,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        serializer.instance = cart_item

class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
