from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notice, NoticeLike, NoticeView
from .serializers import (
    NoticeSerializer,
    NoticeCreateUpdateSerializer,
    NoticeLikeSerializer,
    NoticeViewSerializer
)

# 로그인 유저만 공지사항 목록 조회 가능
class NoticeListView(generics.ListAPIView):
    queryset = Notice.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]


# 로그인 유저만 상세 조회 가능 (조회수 기록 포함)
class NoticeDetailView(generics.RetrieveAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # 로그인 유저일 경우 조회수 기록 (중복 방지)
        NoticeView.objects.get_or_create(user=request.user, notice=instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# 공지사항 등록 (관리자만)
# views.py

class NoticeCreateView(generics.CreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notice = serializer.save(user=request.user)

        # 등록 후 NoticeSerializer로 응답
        response_serializer = NoticeSerializer(notice)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


# 공지사항 수정 (관리자만)
class NoticeUpdateView(generics.UpdateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return NoticeCreateUpdateSerializer
        return NoticeSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(NoticeSerializer(self.get_object()).data)


# 공지사항 삭제 (관리자만)
class NoticeDeleteView(generics.DestroyAPIView):
    queryset = Notice.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "삭제 완료"}, status=status.HTTP_200_OK)


# 공지사항 좋아요 등록/취소 (로그인 유저만)
class NoticeLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notice_id):
        notice = get_object_or_404(Notice, pk=notice_id)
        like, created = NoticeLike.objects.get_or_create(user=request.user, notice=notice)

        if not created:
            like.delete()
            # 좋아요 수 감소
            notice.like_count = NoticeLike.objects.filter(notice=notice).count()
            notice.save()
            return Response({"detail": "좋아요 취소", "like_count": notice.like_count}, status=status.HTTP_200_OK)

        # 좋아요 수 증가
        notice.like_count = NoticeLike.objects.filter(notice=notice).count()
        notice.save()
        return Response({"detail": "좋아요 등록", "like_count": notice.like_count}, status=status.HTTP_201_CREATED)
