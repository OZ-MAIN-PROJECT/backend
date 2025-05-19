from django.urls import include, path
from .views import (CommunityListCreateView, CommunityDetailView, CommunityLikeToggleView,
                    CommentDetailView, CommentListCreateView)


urlpatterns = [
    path('', CommunityListCreateView.as_view(), name='community-list-create'),
    # 게시글 상세 조회, 게시글 수정/삭제
    path('<uuid:community_uuid>/', CommunityDetailView.as_view(), name='community-detail'),
    path('<uuid:community_uuid>/like/', CommunityLikeToggleView.as_view(), name='community-like'),
    path(
        '<uuid:community_uuid>/comment/',
        CommentListCreateView.as_view({'get': 'list', 'post': 'create'}),
        name='comment-list'
    ),
    path(
        '<uuid:community_uuid>/comment/<int:id>/',
        CommentDetailView.as_view(),
        name='comment-detail'
    ),

    # 게시글 좋아요 등록 및 취소
    path('<uuid:community_uuid>/like/', CommunityLikeToggleView.as_view(), name='community-like'),
]