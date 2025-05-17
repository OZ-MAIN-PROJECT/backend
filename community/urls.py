from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CommunityCreateView, CommunityDetailView

urlpatterns = [
    path('', CommunityCreateView.as_view(), name='community-create'),

    path('<uuid:community_uuid>/', CommunityDetailView.as_view(), name='community-detail'),
]