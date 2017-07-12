from rest_framework.pagination import PageNumberPagination
from django.conf import settings

PAGE_SIZE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 30)

class SearchPagination(PageNumberPagination):
    page_size = PAGE_SIZE
