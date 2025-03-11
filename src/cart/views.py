# cart/views.py
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import Cart, CartItem, Purchase
from rest_framework.decorators import action
from .serializers import CartSerializer, CartItemSerializer, PurchaseSerializer
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

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def purchase(self, request, pk=None):
        # Get the specific cart item
        cart_item = self.get_object()
        user = request.user

        # Ensure only customers can purchase items
        if not user.groups.filter(name="customer").exists():
            raise PermissionDenied("Only customers can purchase items.")
        
        package = cart_item.package
        
        # Check stock again (in case stock has changed)
        if cart_item.quantity > package.stock_quantity:
            raise ValidationError("Not enough stock available for this package.")
        
        # Reduce package stock
        package.stock_quantity -= cart_item.quantity
        package.save()
        
        # Create a purchase record with the status "Awaiting admin approval"
        purchase = Purchase.objects.create(
            user=user,
            package=package,
            quantity=cart_item.quantity,
            status="Awaiting admin approval"
        )
        
        # Remove the cart item (simulate a purchase completion)
        cart_item.delete()
        
        serializer = PurchaseSerializer(purchase)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PublicCartItemViewSet(CartItemViewSet):
    permission_classes = [permissions.AllowAny]  # No authentication required

    def get_queryset(self):
        # Return all cart items (for public access, no user filtering)
        return CartItem.objects.all()

class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class PurchaseListView(generics.ListAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)
