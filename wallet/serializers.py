from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet, WalletEmotion, WalletCategory

# 카테고리 필드 중복
class WalletCategoryFieldMixin(serializers.Serializer):
    walletCategory = serializers.PrimaryKeyRelatedField(
        queryset=WalletCategory.objects.all(),
        source='wallet_category'
    )

# 가계부 생성
class WalletCreateSerializer(WalletCategoryFieldMixin, serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = [
            'id', 'type', 'amount', 'title',
            'content', 'walletCategory', 'emotion', 'date'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']


# 가계부 개별 조회
class WalletDetailSerializer(WalletCategoryFieldMixin, serializers.ModelSerializer):
    walletUuid = serializers.UUIDField(source='wallet_uuid')
    createdAt = serializers.DateTimeField(source='created_at')
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        return obj.date if isinstance(obj.date, str) else obj.date.isoformat()
        # 또는 obj.date.strftime('%Y-%m-%d') 도 가능

    class Meta:
        model = Wallet
        fields = [
            'walletUuid', 'type', 'amount', 'title', 'content',
            'date', 'createdAt','walletCategory', 'emotion'
        ]


# 가계부 수정
class WalletUpdateSerializer(WalletCategoryFieldMixin, serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = [
            'amount', 'title',
            'content', 'walletCategory', 'emotion', 'date'
        ]

        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
