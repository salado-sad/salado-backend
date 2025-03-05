from rest_framework import serializers
from .models import Product

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = "__all__"
#
#
class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")  # Owner is read-only and shows username

    class Meta:
        model = Product
        fields = "__all__"
