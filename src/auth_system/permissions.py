from rest_framework.permissions import BasePermission

class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='vendor').exists()

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='customer').exists()

class IsSaladoAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='saladoadmin').exists()

class IsDelivery(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='delivery').exists()
