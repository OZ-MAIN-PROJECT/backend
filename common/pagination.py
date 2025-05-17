import base64
from rest_framework.pagination import BasePagination
from rest_framework.response import Response
from django.utils.encoding import force_str


class CustomCursorPagination(BasePagination):
    page_size = 10
    cursor_query_param = 'cursor'
    ordering = '-id'

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        self.has_next = False
        self.cursor = request.query_params.get(self.cursor_query_param)

        # 커서 디코딩
        if self.cursor:
            try:
                decoded = base64.b64decode(force_str(self.cursor)).decode()
                # 예: 'p=25' → 25
                pk = int(decoded.split('=')[1])
                queryset = queryset.filter(id__lt=pk)  # 역순이니까 id보다 작은 것들만
            except Exception as e:
                print("커서 디코딩 실패:", e)

        # 정렬 및 페이징 처리
        queryset = queryset.order_by(self.ordering)
        results = list(queryset[:self.page_size + 1])  # 다음 페이지 확인 위해 1개 더 가져옴

        if len(results) > self.page_size:
            self.has_next = True
            results = results[:self.page_size]

        self.last_item = results[-1] if results else None
        return results

    def get_paginated_response(self, data):
        next_cursor = None

        if self.has_next and self.last_item:
            # 커서 문자열 직접 생성 (예: "p=21")
            cursor_str = f"p={getattr(self.last_item, 'id')}"
            encoded = base64.b64encode(cursor_str.encode()).decode()
            next_cursor = f"cursor={encoded}"

        return Response({
            'results': data,
            'nextCursor': next_cursor,
            'hasNext': self.has_next
        })
