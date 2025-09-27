from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20                 # default per page ["page.paginator.count", "20"]
    page_size_query_param = "page_size"  # allow ?page_size=50
    max_page_size = 100

