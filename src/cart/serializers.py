from rest_framework import serializers
from management.models import Package
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    package = serializers.StringRelatedField(read_only=True)
    package_id = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all(), source='package', write_only=True)
    cost = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'package', 'package_id', 'quantity', 'cost']
        read_only_fields = ['id', 'cost', 'package']

    def get_cost(self, obj):
        return obj.get_cost()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_cost']
        read_only_fields = ['id', 'user', 'total_cost']

    def get_total_cost(self, obj):
        return obj.get_total_cost()
