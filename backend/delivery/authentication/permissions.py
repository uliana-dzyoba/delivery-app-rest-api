from rest_framework import permissions

class IsOwnerPermission(permissions.BasePermission):
    # for view permission
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # for object level permissions
    def has_object_permission(self, request, view, order_obj):
        if request.method == 'PUT' or request.method == 'PATCH':
            return request.user.is_staff
        return order_obj.customer.id == request.user.id