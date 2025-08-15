from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsWarehouseManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['admin', 'warehouse_manager']