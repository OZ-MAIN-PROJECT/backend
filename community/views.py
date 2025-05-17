import math

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import BasePermission

from common.pagination import CustomPageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Community, CommunityLike, CommunityView
from .serializers import (
    CommunitySerializer,
    CommunityCreateUpdateSerializer,
    CommunityLikeSerializer,
    CommunityViewSerializer
)

class IsAdminForNoticeType(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PATCH', 'PUT']:
            # PATCH 시에는 body에 type이 없을 수 있으므로 fallback
            type_ = request.data.get('type')
            if not type_ and hasattr(view, 'get_object'):
                try:
                    type_ = view.get_object().type
                except:
                    pass

            if type_ == 'NOTICE':
                return request.user.is_staff or request.user.role == 'ADMIN'
        return True

# 커뮤니티 글 등록
class CommunityListCreateView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Community.objects.all().order_by('-created_at')
    serializer_class = CommunitySerializer
    pagination_class = CustomPageNumberPagination
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminForNoticeType()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommunityCreateUpdateSerializer
        return CommunitySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        post_type = self.request.query_params.get('type')
        if post_type:
            queryset = queryset.filter(type=post_type)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        community = serializer.save(user=request.user)

        # 등록 후 CommunitySerializer로 응답
        response_serializer = CommunitySerializer(community, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

# 로그인 유저만 상세 조회 가능 (조회수 기록 포함)
class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    lookup_field = 'community_uuid'
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            return [IsAdminForNoticeType()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return CommunityCreateUpdateSerializer
        return CommunitySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # 로그인 유저일 경우 조회수 기록 (중복 방지)
        CommunityView.objects.get_or_create(user=request.user, community=instance)

        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        print("🔧 PATCH 호출됨")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = super().update(request, *args, **kwargs)
        return Response(CommunitySerializer(self.get_object(), context={"request": request}).data)

    def destroy(self, request, *args, **kwargs):
        print("🧨 DELETE 호출됨")
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)






# 커뮤니티 좋아요 등록/취소
class CommunityLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, community_id):
        community = get_object_or_404(Community, pk=community_id)
        like, created = CommunityLike.objects.get_or_create(user=request.user, community=community)

        if not created:
            return Response({"detail": "이미 좋아요가 되어 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        community.likes = CommunityLike.objects.filter(community=community).count()
        community.save()
        return Response({"detail": "좋아요 등록", "like_count": community.likes, "is_liked": True}, status=status.HTTP_201_CREATED)

    def delete(self, request, community_id):
        community = get_object_or_404(Community, pk=community_id)
        like = CommunityLike.objects.filter(user=request.user, community=community).first()

        if not like:
            return Response({"detail": "좋아요가 되어 있지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        community.likes = CommunityLike.objects.filter(community=community).count()
        community.save()
        return Response({"detail": "좋아요 취소", "like_count": community.likes, "is_liked": False}, status=status.HTTP_200_OK)
