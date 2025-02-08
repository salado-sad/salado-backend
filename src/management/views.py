from rest_framework import viewsets
from rest_framework.response import Response
from .models import Package, PackageProduct
from .serializers import PackageSerializer
from vendors.models import Product
from rest_framework import status

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        package = Package.objects.create(
            name=data["name"],
            price=data["price"],
            description=data.get("description", ""),
            image=data.get("image", None),
        )

        for product in data.get("products", []):
            product_instance = Product.objects.get(id=product["product_id"])
            PackageProduct.objects.create(
                package=package, product=product_instance, quantity=product["quantity"]
            )

        serializer = PackageSerializer(package)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
