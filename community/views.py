import math
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from common.pagination import CustomPageNumberPagination
from .models import Community, CommunityLike, CommunityView, Comment
from .serializers import (
    CommunitySerializer,
    CommunityCreateUpdateSerializer,
    CommunityLikeSerializer,
    CommunityViewSerializer,
    CommentCreateUpdateSerializer,
    CommentReplySerializer
)


# 공지사항 작성 권한 확인용 커스텀 Permission 클래스
class IsAdminForNoticeType(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PATCH', 'PUT']:
            # PATCH 시에는 body에 type이 없을 수 있으므로 fallback 처리
            type_ = request.data.get('type')
            if not type_ and hasattr(view, 'get_object'):
                try:
                    type_ = view.get_object().type
                except:
                    pass
            if type_ == 'NOTICE':
                return request.user.is_staff or request.user.role == 'ADMIN'
        return True


# 게시글 목록 조회, 게시글 등록
class CommunityListCreateView(generics.ListCreateAPIView):
    queryset = Community.objects.all().order_by('-created_at')
    pagination_class = CustomPageNumberPagination
    parser_classes = [MultiPartParser, FormParser]

    # POST 요청일 경우에는 공지 권한 검사
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminForNoticeType()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommunityCreateUpdateSerializer
        return CommunitySerializer

    # 게시판 타입 쿼리 파라미터로 필터링
    def get_queryset(self):
        queryset = super().get_queryset()
        post_type = self.request.query_params.get('type')
        if post_type:
            queryset = queryset.filter(type=post_type)
        return queryset

    # 유저 정보를 저장할 수 있게 수정
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 게시글 상세 조회, 게시글 수정/삭제
class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    lookup_field = 'community_uuid'  # 🔄 uuid 기반으로 조회
    parser_classes = [MultiPartParser, FormParser]

    # 공지 수정은 관리자 권한 필요
    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            return [IsAdminForNoticeType()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return CommunityCreateUpdateSerializer
        return CommunitySerializer

    # 조회 시 조회수 기록
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        CommunityView.objects.get_or_create(user=request.user, community=instance)
        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)
    
    # 게시글 수정
    def update(self, request, *args, **kwargs):
        print("🔧 PATCH 호출됨")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(CommunitySerializer(instance, context={"request": request}).data)
        self.perform_update(serializer)
        return Response(CommunitySerializer(instance, context={"request": request}).data)

    # 삭제 요청 처리
    def destroy(self, request, *args, **kwargs):
        print("🧨 DELETE 호출됨")
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# 좋아요 등록/취소
class CommunityLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 좋아요 등록 (중복 방지)
    def post(self, request, community_uuid):
        community = get_object_or_404(Community, community_uuid=community_uuid)  # 🔄 pk → uuid
        like, created = CommunityLike.objects.get_or_create(user=request.user, community=community)

        if not created:
            return Response({"detail": "이미 좋아요가 되어 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        community.likes = CommunityLike.objects.filter(community=community).count()
        community.save()
        return Response({"detail": "좋아요 등록", "like_count": community.likes, "is_liked": True}, status=status.HTTP_201_CREATED)

    # 좋아요 취소
    def delete(self, request, community_uuid):
        community = get_object_or_404(Community, community_uuid=community_uuid)
        like = CommunityLike.objects.filter(user=request.user, community=community).first()

        if not like:
            return Response({"detail": "좋아요가 되어 있지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        community.likes = CommunityLike.objects.filter(community=community).count()
        community.save()
        return Response({"detail": "좋아요 취소", "like_count": community.likes, "is_liked": False}, status=status.HTTP_200_OK)
    

# 댓글/대댓글 조회 및 등록
class CommentListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 댓글/대댓글 전체 조회
    def get(self, request, community_uuid):
        community = get_object_or_404(Community, community_uuid=community_uuid)

        # 최상위 댓글만 조회 (parent_comment_id가 null인 댓글)
        top_comments = Comment.objects.filter(
            community=community,
            parent_comment_id__isnull=True
        ).select_related('user').prefetch_related('replies__user').order_by('created_at')

        serializer = CommentReplySerializer(top_comments, many=True)
        return Response({
            "community_uuid": str(community.community_uuid),
            "comment_replies": serializer.data
        })
    # 댓글/대댓글 등록
    def post(self, request, community_uuid):
        community = get_object_or_404(Community, community_uuid=community_uuid)
        serializer = CommentCreateUpdateSerializer(
            data=request.data,
            context={'request': request, 'community': community}
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response(CommentReplySerializer(comment).data, status=status.HTTP_201_CREATED)


# 댓글/대댓글 수정 및 삭제
class CommentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 작성자 본인 확인
    def get_object(self, comment_id, user):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user != user:
            raise PermissionDenied("본인의 댓글만 수정/삭제할 수 있습니다.")
        return comment

    # 댓글/대댓글 수정
    def patch(self, request, community_uuid, comment_id):
        comment = self.get_object(comment_id, request.user)
        serializer = CommentCreateUpdateSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_comment = serializer.save()
        return Response(CommentReplySerializer(updated_comment).data)

    # 댓글/대댓글 삭제
    def delete(self, request, community_uuid, comment_id):
        comment = self.get_object(comment_id, request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)