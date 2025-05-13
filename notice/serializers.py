from rest_framework import serializers
from .models import Notice, NoticeLike, NoticeView
from users.models import User


# 공지사항 조회 (목록, 상세) 
class NoticeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    view_count = serializers.SerializerMethodField() # 조회수 필드 (조회수는 NoitceView에서 계산)

    class Meta:
        model = Notice
        fields = [
            'notice_id',
            'user',
            'title',
            'content',
            'like_count',
            'view_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['notice_id', 'user', 'like_count', 'view_count', 'created_at', 'updated_at']

    # 조회수 필드 처리 메서드 (SerializerMethodField용)
    def get_view_count(self, obj):
        return NoticeView.objects.filter(notice=obj).count()


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
