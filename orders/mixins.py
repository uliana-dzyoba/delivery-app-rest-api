from datetime import datetime, timedelta
from django.utils.timezone import make_aware


def parameter_to_date(parameter):
    # parameter is in a format "yyyy-mm-dd"
    date_list = [int(x) for x in parameter.split('-')]
    if len(date_list) == 3:
        date = make_aware(datetime(*date_list))
    return date


class OrderStatusDateFilterMixin(object):
    # mixin for filtering by status, specific date and date range
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        status = self.request.query_params.get('status')
        if status is not None:
            qs = qs.filter(order_status=status.upper())

        date = self.request.query_params.get('date')
        if date is not None:
            exact_date = parameter_to_date(date)
            end_date = exact_date + timedelta(days=1)
            qs = qs.filter(delivery_at__range=[exact_date, end_date])

        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')
        if from_date is not None and to_date is not None:
            start_date = parameter_to_date(from_date)
            end_date = parameter_to_date(to_date) + timedelta(days=1)
            qs = qs.filter(delivery_at__range=[start_date, end_date])

        return qs
