from rest_framework import filters


class SimpleFilterBackend(filters.BaseFilterBackend):
    """A simple filter backend, filtering on all fields specified in
    View filter_fields.
    """

    @staticmethod
    def get_request_filters(request):
        return request.query_params.copy()

    def filter_queryset(self, request, queryset, view):
        filter_kwargs = {}
        for k, v in self.get_request_filters(request).items():
            if k in view.filter_fields:
                filter_kwargs[k] = v
        if filter_kwargs:
            return queryset.filter(**filter_kwargs)
        return queryset
