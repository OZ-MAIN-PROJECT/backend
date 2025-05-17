from rest_framework import serializers
from .models import Notice, NoticeLike, NoticeView



# 공지사항 조회 (목록, 상세) 
from rest_framework import serializers
from notice.models import Notice, NoticeView

class NoticeSerializer(serializers.ModelSerializer):
    notice_id = serializers.IntegerField(source='id')
    user_id = serializers.UUIDField(source='user.user_id', read_only=True)
    likes = serializers.IntegerField(source='like_count', read_only=True)
    views = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = [
            'notice_id',
            'user_id',
            'title',
            'content',
            'likes',
            'views',
            'is_liked',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields

    def get_views(self, obj):
        return NoticeView.objects.filter(notice=obj).count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return NoticeLike.objects.filter(user=user, notice=obj).exists()



# 공지사항 등록/수정
class NoticeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['title', 'content']


# 공지사항 좋아요 기록 기능
class NoticeLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    notice = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = NoticeLike
        fields = ['like_id', 'user', 'notice', 'created_at']
        read_only_fields = ['like_id', 'user', 'notice', 'created_at']


# 공지사항 조회 기록 기능
class NoticeViewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    notice = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = NoticeView
        fields = ['view_id', 'user', 'notice', 'viewed_at']
        read_only_fields = ['view_id', 'user', 'notice', 'viewed_at']