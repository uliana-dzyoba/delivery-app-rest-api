def paginate_objects(request, paginator, objects, serializer_class):
    page = paginator.paginate_queryset(objects, request)
    if page is not None:
        serializer = serializer_class(page, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return response
