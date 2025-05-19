from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CommunityListCreateView, CommunityDetailView,CommunityLikeToggleView,CommentListCreateView,CommentDetailView

router = DefaultRouter()
router.register(r'', CommunityListCreateView, basename='community')

urlpatterns = [
    path('', include(router.urls)),
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
]