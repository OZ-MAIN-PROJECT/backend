from rest_framework import serializers

from common.image.models import Image
from community.models import Community, CommunityLike, CommunityView


# 커뮤니티 조회 (목록, 상세)
class CommunitySerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = [
            'community_uuid',
            'nickname',
            'type',
            'title',
            'content',
            'likes',
            'views',
            'is_liked',
            'is_owner',
            'image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields

    def get_nickname(self, obj):
        return obj.user.nickname

    def get_views(self, obj):
        return CommunityView.objects.filter(community=obj).count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return CommunityLike.objects.filter(user=user, community=obj).exists()
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            return False
        return obj.user == request.user

    def get_image(self, obj):
        image = Image.objects.filter(ref_type=obj.type, ref_id=obj.id).first()
        return image.url if image else None


# 커뮤니티 등록/수정
class CommunityCreateUpdateSerializer(serializers.ModelSerializer):
    image = serializers.URLField(write_only=True, required=False)


    class Meta:
        model = Community
        fields = ['title', 'content', 'type', 'image']

    def create(self, validated_data):
        image_url = validated_data.pop('image', None)
        community = super().create(validated_data)

        if image_url:
            Image.objects.create(
                ref_type=community.type,
                ref_id=community.id,
                url=image_url,  # ✅ DB엔 'url' 필드에 저장
                user=self.context['request'].user
            )

        return community

    def update(self, instance, validated_data):
        print("업데이트 데이터:", validated_data)

        image_url = validated_data.pop('image', None)

        print("남은 데이터:", validated_data)
        community = super().update(instance, validated_data)

        if image_url:
            Image.objects.update_or_create(
                ref_type=community.type,
                ref_id=community.id,
                defaults={'url': image_url}
            )

        return community


# 커뮤니티 좋아요 기록 기능
class CommunityLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    community = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CommunityLike
        fields = ['like_id', 'user', 'community', 'created_at']
        read_only_fields = ['like_id', 'user', 'community', 'created_at']


# 커뮤니티 조회 기록 기능
class CommunityViewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    community = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CommunityView
        fields = ['view_id', 'user', 'community', 'viewed_at']
        read_only_fields = ['view_id', 'user', 'community', 'viewed_at']
