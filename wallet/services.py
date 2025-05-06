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


def get_wallet_detail(user, wallet_uuid):
    try:
        wallet = Wallet.objects.get(user=user, wallet_uuid=wallet_uuid)
        return wallet
    except Exception as e:
        print("💥 Wallet 개별 조회 오류:", e)
        raise ValidationError({"detail": f"지갑 조회 실패: {str(e)}"})


def update_wallet(user, wallet_uuid, data):
    try:
        wallet = Wallet.objects.get(user=user, wallet_uuid=wallet_uuid)

        wallet.amount = data['amount']
        wallet.title = data['title']
        wallet.content = data['content']
        wallet.wallet_category = data['wallet_category']
        wallet.emotion = data['emotion']
        wallet.date = data['date']
        wallet.save()

        return wallet


    except Wallet.DoesNotExist:
        raise ValidationError({"detail": "정보를 찾을 수 없습니다."})
    except Exception as e:
        raise ValidationError({"detail": f"수정 실패: {str(e)}"})

