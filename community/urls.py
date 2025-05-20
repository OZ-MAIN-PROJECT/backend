from django.urls import path

from common.image.imageView import ImageUploadView

from .views import (
    CommunityListCreateView,
    CommunityDetailView,
    CommunityLikeToggleView,
    CommentListCreateView,
    CommentDetailView
)

urlpatterns = [
    # 게시글 목록 조회, 게시글 등록
    path('', CommunityListCreateView.as_view(), name='community-list-create'),

    # 게시글 상세 조회, 게시글 수정/삭제
    path('<uuid:community_uuid>/', CommunityDetailView.as_view(), name='community-detail'),

    # 게시글 좋아요 등록 및 취소
    path('<uuid:community_uuid>/like/', CommunityLikeToggleView.as_view(), name='community-like'),

    # 댓글/대댓글 등록 및 목록 조회
    path('<uuid:community_uuid>/comment/', CommentListCreateView.as_view(), name='comment-list-create'),

    # 댓글/대댓글 수정 및 삭제
    path('<uuid:community_uuid>/comment/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),

    path('image/', ImageUploadView.as_view(), name='image-upload'),
]