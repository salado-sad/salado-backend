from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from .models import Package
from vendors.models import Product
from .serializers import PackageSerializer
from decimal import Decimal

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a package, ensure enough stock exists (for the entire package stock quantity), and reduce stock.
        """
        data = request.data
        products = data.get("products", [])
        package_stock_quantity = data.get("stock_quantity", 1)  # Number of package units being created

        if not products:
            return Response({"error": "Products field is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check stock for all products
        insufficient_stock = []
        for item in products:
            product_id = item.get("product_id")
            item_quantity_per_package = item.get("quantity", 1)
            total_required_quantity = item_quantity_per_package * package_stock_quantity  # Adjust for total package stock

            try:
                product = Product.objects.get(id=product_id)
                if product.stock_quantity < total_required_quantity:
                    insufficient_stock.append({
                        "product_id": product_id,
                        "available_stock": product.stock_quantity,
                        "required_stock": total_required_quantity
                    })
            except Product.DoesNotExist:
                return Response({"error": f"Product with ID {product_id} does not exist"},
                                status=status.HTTP_400_BAD_REQUEST)

        # If stock is not sufficient, return error
        if insufficient_stock:
            return Response({
                "error": "Insufficient stock for the following products",
                "details": insufficient_stock
            }, status=status.HTTP_400_BAD_REQUEST)

        # Reduce stock if all products have enough stock
        with transaction.atomic():
            package = Package.objects.create(
                name=data["name"],
                stock_quantity=package_stock_quantity,
                description=data.get("description", ""),
                image=data.get("image", None),
                products=products
            )

            # Reduce stock of each product
            for item in products:
                product = Product.objects.get(id=item["product_id"])
                product.stock_quantity -= item["quantity"] * package_stock_quantity
                product.save()

            package.save()

        serializer = PackageSerializer(package)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
