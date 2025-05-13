from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Count, Sum
from rest_framework.exceptions import ValidationError

from statistic.models import MonthlyStatistic
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
            .annotate(count=Count("id"),
                      amount=Sum("amount")
            ).order_by("-count")
        )

        result = []
        for stat in emotion_stats:
            percentage = (Decimal(stat['count']) / Decimal(total_count)) * 100
            rounded_percentage = percentage.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
            result.append({
                'emotion': stat['emotion'],
                'rate': float(rounded_percentage),
                'amount' : stat['amount']
            })



        return result

    except Exception as e:
        print("💥 Wallet 월별 감정 통계 조회 오류:", e)
        raise ValidationError({"detail": f"월별 감정 통계 조회 실패: {str(e)}"})


def get_category_statistic(user, year, month):
    try:

        queryset = Wallet.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        )

        total_count = queryset.count()
        if total_count == 0:
            return []

        emotion_stats = (
            queryset
            .values("wallet_category")
            .annotate(count=Count("id"),
                      amount=Sum("amount")
                      ).order_by("-count")
        )

        result = []
        for stat in emotion_stats:
            percentage = (Decimal(stat['count']) / Decimal(total_count)) * 100
            rounded_percentage = percentage.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
            result.append({
                'category': stat['wallet_category'],
                'rate': float(rounded_percentage),
                'amount': stat['amount']
            })

        return result

    except Exception as e:
        print("💥 Wallet 월별 카테고리 통계 조회 오류:", e)
        raise ValidationError({"detail": f"월별 카테고리 통계 조회 실패: {str(e)}"})

def create_monthly_statistic(user, year, month):
    total_income = Wallet.objects.filter(
        user=user,
        date__year=year,
        date__month=month,
        type='INCOME'
    ).aggregate(total=Sum('amount'))['total'] or 0


    total_expense = Wallet.objects.filter(
        user=user,
        date__year=year,
        date__month=month,
        type='EXPENSE'
    ).aggregate(total=Sum('amount'))['total'] or 0

    stat_exists = MonthlyStatistic.objects.filter(
        user=user, year=year, month=month
    ).exists()

    if not stat_exists:
        MonthlyStatistic.objects.create(
            user=user,
            year=year,
            month=month,
            total_income=total_income,
            total_expense=total_expense
        )
    else:
        print(f"⚠️ {user.email}: 이미 {year}-{month} 통계 존재함. 저장 생략.")