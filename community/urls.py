from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommunityViewSet

router = DefaultRouter()
router.register(r'community', CommunityViewSet, basename='community')

urlpatterns = [
    path('', include(router.urls)),
]