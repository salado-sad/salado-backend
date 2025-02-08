from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Package
from .serializers import PackageSerializer

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a package with product names and quantities directly in JSONField.
        """
        data = request.data
        package = Package.objects.create(
            name=data["name"],
            price=data["price"],
            description=data.get("description", ""),
            image=data.get("image", None),
            products=data["products"]  # List of product details
        )

        serializer = PackageSerializer(package)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
