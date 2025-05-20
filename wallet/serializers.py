from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet, WalletEmotion, WalletCategory

# 가계부 생성
class WalletCreateSerializer( serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = [
            'id', 'type', 'amount', 'title',
            'content', 'wallet_category', 'emotion', 'date'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']


# 가계부 개별 조회
class WalletDetailSerializer( serializers.ModelSerializer):
    walletUuid = serializers.UUIDField(source='wallet_uuid')
    createdAt = serializers.DateTimeField(source='created_at')
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        return obj.date.date() if hasattr(obj.date, 'date') else obj.date

    class Meta:
        model = Wallet
        fields = [
            'walletUuid', 'type', 'amount', 'title', 'content',
            'date', 'createdAt','wallet_category', 'emotion'
        ]

        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'date']


# 가계부 수정
class WalletUpdateSerializer( serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = [
            'amount', 'title',
            'content', 'wallet_category', 'emotion', 'date'
        ]

        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
