from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from wallet.models import Wallet, WalletCategory, WalletEmotion

def create_wallet(user,data) :
    try:
        return Wallet.objects.create(
            user=user,
            type=data['type'],
            amount=data['amount'],
            title=data['title'],
            content=data['content'],
            wallet_category=data['wallet_category'],
            emotion=data['emotion'],
            date=data['date']
        )
    except Exception as e:
        print("💥 Wallet 생성 오류:", e)
        raise ValidationError({"detail": f"지갑 생성 실패: {str(e)}"})