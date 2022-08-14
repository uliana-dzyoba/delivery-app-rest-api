from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    # for view permission
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, order_obj):
        if request.user.is_staff:
            return True
        if request.method in ['PUT', 'PATCH']:
            return False
        return order_obj.customer.id == request.user.id


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff