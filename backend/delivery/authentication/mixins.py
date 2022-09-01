class UserQuerySetMixin(object):
    # mixin for query of a current user
    user_field = 'customer'
    allow_staff_view = True

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {self.user_field: user}
        qs = super().get_queryset(*args, **kwargs)
        if self.allow_staff_view and user.is_staff:
            return qs
        return qs.filter(**lookup_data)


