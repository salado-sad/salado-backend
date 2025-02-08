from django.db import models
from vendors.models import Product  # Import Product model

class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="package_images/", blank=True, null=True)

    def __str__(self):
        return self.name

class PackageProduct(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Stores how many of each product is in the package

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.package.name}"
