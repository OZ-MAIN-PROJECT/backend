from rest_framework import serializers
from .models import Community, Comment


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        # id, type, title, content, image, created_at, updated_at 등 필요한 필드만 나열
        fields = '__all__'
        read_only_fields = ['user']

class CommentSerializer(serializers.ModelSerializer):
    # user 필드는 읽기 전용(CurrentUserDefault), 생성 시 perform_create 에서 자동 저장
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    # 어느 게시글(comment.community)에 속한 댓글인지
    community = serializers.PrimaryKeyRelatedField(
        queryset=Community.objects.all()
    )
    # 대댓글 기능: 부모 댓글이 있을 수도, 없을 수도
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'community',
            'user',
            'parent',
            'content',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']