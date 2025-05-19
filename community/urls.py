from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CommunityListCreateView, CommunityDetailView, CommunityLikeToggleView

router = DefaultRouter()
router.register(r'', CommunityListCreateView, basename='community')

urlpatterns = [
    path('', include(router.urls)),  # ✅ router만 사용
    # 게시글 상세/수정/삭제
    path('<uuid:community_uuid>/', CommunityDetailView.as_view(), name='community-detail'),
    path('<uuid:communtiy_uuid>/like/', CommunityLikeToggleView.as_view(), name='community-like'),
]