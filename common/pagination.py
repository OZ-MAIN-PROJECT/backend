import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        total_pages = math.ceil(self.page.paginator.count / self.page.paginator.per_page)
        return Response({
            'results': data,
            'page': self.page.number,
            'size': self.page.paginator.per_page,
            'totalPages': total_pages,
            'totalElements': self.page.paginator.count,
        })