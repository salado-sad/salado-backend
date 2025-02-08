from rest_framework import serializers
from .models import Package, PackageProduct
from vendors.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "image"]

class PackageProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = PackageProduct
        fields = ["product", "quantity"]

class PackageSerializer(serializers.ModelSerializer):
    products = PackageProductSerializer(source="packageproduct_set", many=True, read_only=True)

    class Meta:
        model = Package
        fields = ["id", "name", "price", "description", "image", "products"]
