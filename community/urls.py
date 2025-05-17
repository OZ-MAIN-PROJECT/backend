from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CommunityListCreateView, CommunityDetailView

router = DefaultRouter()
router.register(r'', CommunityListCreateView, basename='community')

urlpatterns = [
    path('', include(router.urls)),  # ✅ router만 사용
    path('<uuid:community_uuid>/', CommunityDetailView.as_view(), name='community-detail'),
]