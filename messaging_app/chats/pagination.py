from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20                 # default per page
    page_size_query_param = "page_size"  # allow ?page_size=50
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "page_size": self.get_page_size(self.request),  #  items will default to 20 ["page.paginator.count", "20"]
            "current_page": self.page.number,
            "total_pages": self.page.paginator.num_pages,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })
