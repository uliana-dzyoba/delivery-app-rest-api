from rest_framework import permissions


class IsAdminOrIsOwnerReadOnly(permissions.BasePermission):
    # permission for owner to view and for the staff to modify
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, order_obj):
        if request.method in permissions.SAFE_METHODS:
            return order_obj.customer.id == request.user.id
        return request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
