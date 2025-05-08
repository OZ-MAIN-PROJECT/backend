from rest_framework import viewsets
from .models import Community
from .serializers import CommunitySerializer

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all().order_by('-created_at')
    serializer_class = CommunitySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        post_type = self.request.query_params.get('type')
        if post_type:
            queryset = queryset.filter(type=post_type)
        return queryset