from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

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
        cart, _ = Cart.objects.get_or_create(user=user)
        package = serializer.validated_data['package']
        quantity = serializer.validated_data.get('quantity', 1)
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
