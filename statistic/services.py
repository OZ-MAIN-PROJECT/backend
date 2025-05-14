from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Count, Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from statistic.models import MonthlyStatistic
from wallet.models import Wallet

def get_emotion_statistic(user, year, month):
    try:
        queryset = Wallet.objects.filter(
            user=user,
            date__year=year,
            date__month=month,
            type="EXPENSE"
        ).exclude(emotion__isnull=True).exclude(emotion="")

        total_amount = queryset.aggregate(total=Sum("amount"))["total"]
        if not total_amount or total_amount == 0:
            return []

        emotion_stats = (
            queryset
            .values("emotion")
            .annotate(
                count=Count("id"),
                amount=Sum("amount")
            )
            .order_by("-amount")
        )

        result = []
        total_amount_decimal = Decimal(str(total_amount))
        for stat in emotion_stats:
            amount_decimal = Decimal(str(stat['amount']))
            percentage = (amount_decimal / total_amount_decimal) * 100
            rounded_percentage = percentage.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

            result.append({
                'emotion': stat['emotion'],
                'rate': float(rounded_percentage),  # 금액 기준 비율
                'amount': stat['amount'],
                'count': stat['count']              # 원하면 제외 가능
            })

        return { "emotionStatistics": result }

    except Exception as e:
        print("💥 Wallet 월별 감정 통계 조회 오류:", e)
        raise ValidationError({"detail": f"월별 감정 통계 조회 실패: {str(e)}"})


def get_category_statistic(user, year, month):
    try:
        queryset = Wallet.objects.filter(
            user=user,
            date__year=year,
            date__month=month,
            type="EXPENSE"
        ).exclude(wallet_category__isnull=True).exclude(wallet_category="")

        total_amount = queryset.aggregate(total=Sum("amount"))["total"]
        if not total_amount or total_amount == 0:
            return []

        wallet_category_stats = (
            queryset
            .values("wallet_category")
            .annotate(
                count=Count("id"),
                amount=Sum("amount")
            )
            .order_by("-amount")
        )

        result = []
        total_amount_decimal = Decimal(str(total_amount))
        for stat in wallet_category_stats:
            amount_decimal = Decimal(str(stat['amount']))
            percentage = (amount_decimal / total_amount_decimal) * 100
            rounded_percentage = percentage.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

            result.append({
                'category': stat['wallet_category'],
                'rate': float(rounded_percentage),  # 금액 기준 비율
                'amount': stat['amount'],
                'count': stat['count']  # 원하면 제외 가능
            })

        return { "categoryStatistics": result }

    except Exception as e:
        print("💥 Wallet 월별 감정 통계 조회 오류:", e)
        raise ValidationError({"detail": f"월별 감정 통계 조회 실패: {str(e)}"})

def get_monthly_statistic(user, year):
    try:

        stats = MonthlyStatistic.objects.filter(
            user=user,
            year=year
        )

        # 월별로 매핑 (1~12)
        month_map = {stat.month: stat for stat in stats}

        monthly_stats = []
        for month in range(1, 13):
            stat = month_map.get(month)
            monthly_stats.append({
                "month": month,
                "incomeAmount": stat.total_income if stat else 0,
                "expenseAmount": stat.total_expense if stat else 0,
            })
        return {
            "year": year,
            "monthlyStatistics": monthly_stats
        }
    except Exception as e:
        print("💥 Wallet 월별 감정 통계 조회 오류:", e)
        raise ValidationError({"detail": f"월별 감정 통계 조회 실패: {str(e)}"})

@receiver([post_save, post_delete], sender=Wallet)
def update_monthly_statistic(sender, instance, **kwargs):
    user = instance.user
    date = instance.date
    year = date.year
    month = date.month

    # 월별 전체 수입, 지출 계산
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

    # 기존 통계가 있으면 업데이트, 없으면 생성
    stat, created = MonthlyStatistic.objects.get_or_create(
        user=user, year=year, month=month,
        defaults={'total_income': total_income, 'total_expense': total_expense}
    )

    if not created:
        stat.total_income = total_income
        stat.total_expense = total_expense
        stat.save()

    else:
        print(f"⚠️ {user.email}: 이미 {year}-{month} 통계 존재함. 저장 생략.")