from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Community
from .serializers import CommunitySerializer

class CommunityViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]


    queryset = Community.objects.all().order_by('-created_at')
    serializer_class = CommunitySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        post_type = self.request.query_params.get('type')
        if post_type:
            queryset = queryset.filter(type=post_type)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)