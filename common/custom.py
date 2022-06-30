from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "items_per_page"  # items per page

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "total": self.get_page_size(self.request),
                "current_page": int(self.request.GET.get("page")) if self.request.GET.get("page") else 1,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data
            }
        )
