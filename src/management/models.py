from django.db import models
from decimal import Decimal
from vendors.models import Product

class Package(models.Model):
    name = models.CharField(max_length=255)
    stock_quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="package_images/", blank=True, null=True)
    products = models.JSONField(default=list, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def calculate_price(self):
        total = Decimal("0.00")

        for item in self.products:
            product_id = item.get("product_id")
            quantity = Decimal(item.get("quantity", 1))

            try:
                product = Product.objects.get(id=product_id)
                total += Decimal(str(product.price)) * quantity
            except Product.DoesNotExist:
                continue

        return total * Decimal("1.2")  # Apply multiplier if needed

    def save(self, *args, **kwargs):
        self.price = self.calculate_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
