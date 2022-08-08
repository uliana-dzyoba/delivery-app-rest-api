from rest_framework import permissions

class IsOwnerPermission(permissions.BasePermission):
    # for view permission
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, order_obj):
        if request.user.is_staff:
            return True
        if request.method == 'PUT' or request.method == 'PATCH':
            return False
        return order_obj.customer.id == request.user.id