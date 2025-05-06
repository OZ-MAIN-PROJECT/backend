from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet, WalletEmotion, WalletCategory


# 가계부 생성
class WalletCreateSerializer(serializers.ModelSerializer):
    walletCategory = serializers.PrimaryKeyRelatedField(
        queryset=WalletCategory.objects.all(),
        source='wallet_category'
    )


    class Meta:
        model = Wallet
        fields = [
            'id', 'type', 'amount', 'title',
            'content', 'walletCategory', 'emotion', 'date'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']


# 가계부 개별 조회
class WalletDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'