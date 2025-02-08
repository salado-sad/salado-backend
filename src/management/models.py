from django.db import models

class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="package_images/", blank=True, null=True)
    products = models.JSONField(default=list)  # Stores product names and quantities as JSON

    def __str__(self):
        return self.name
