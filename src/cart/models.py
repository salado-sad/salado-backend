from django.db import models
from django.conf import settings
from management.models import Package
from decimal import Decimal

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total_cost(self):
        total = Decimal("0.00")
        for item in self.items.all():
            total += item.get_cost()
        return total

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.package.price * self.quantity

    def __str__(self):
        return f"{self.package.name} (x{self.quantity}) in {self.cart.user.username}'s cart"
    

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchases")
    package = models.ForeignKey("management.Package", on_delete=models.CASCADE)  # adjust the import if needed
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=50, default="Awaiting admin approval")
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase of {self.package.name} (x{self.quantity}) by {self.user.username}"
