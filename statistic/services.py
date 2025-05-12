from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework.exceptions import ValidationError

from wallet.models import Wallet


def get_emotion_statistic(user, year, month):
    try:

        queryset = Wallet.objects.filter(
            user = user,
            date__year=year,
            date__month=month
        )

        total_count = queryset.count()
        if total_count == 0:
            return []


        emotion_stats = (
            queryset
            .values("emotion")
            .annotate(count=Count("id"))
        )

        result = []
        for stat in emotion_stats:
            percentage = (Decimal(stat['count']) / Decimal(total_count)) * 100
            rounded_percentage = percentage.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
            result.append({
                'emotion': stat['emotion'],
                'percentage': float(rounded_percentage)
            })



        return result

    except Exception as e:
        print("💥 Wallet 월별 감정 통계 조회 오류:", e)
        raise ValidationError({"detail": f"월별 감정 통계 조회 실패: {str(e)}"})