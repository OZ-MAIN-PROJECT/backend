from django.urls import path
from .views import (
    CommunityListCreateView,
    CommunityDetailView,
    CommunityLikeToggleView,
)

urlpatterns = [
    # 게시글 목록 조회, 게시글 등록
    path('', CommunityListCreateView.as_view(), name='community-list-create'),

    # 게시글 상세 조회, 게시글 수정/삭제
    path('<uuid:community_uuid>/', CommunityDetailView.as_view(), name='community-detail'),

    # 게시글 좋아요 등록 및 취소
    path('<uuid:community_uuid>/like/', CommunityLikeToggleView.as_view(), name='community-like'),
]