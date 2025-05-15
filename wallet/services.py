from collections import defaultdict

from django.core.paginator import Paginator
from django.db.models import Sum, Window, F, Q
from django.db.models.functions import RowNumber, TruncDate
from rest_framework.exceptions import ValidationError
from calendar import monthrange
from datetime import date, timedelta, datetime
from wallet.models import Wallet

# 가계부 생성
def create_wallet(user,data) :
    try:
        return Wallet.objects.create(
            user=user,
            type=data['type'],
            amount=data['amount'],
            title=data['title'],
            content=data['content'],
            wallet_category=data['wallet_category'],
            emotion =data['emotion'],
            date=data['date']
        )
    except Exception as e:
        print("💥 Wallet 생성 오류:", e)
        raise ValidationError({"detail": f"가계부 생성 실패: {str(e)}"})

# 가계부 개별 조회
def get_wallet_detail(user, wallet_uuid):
    try:
        wallet = Wallet.objects.get(user=user, wallet_uuid=wallet_uuid)
        return wallet
    except Exception as e:
        print("💥 Wallet 개별 조회 오류:", e)
        raise ValidationError({"detail": f"가계부 조회 실패: {str(e)}"})


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
        raise ValidationError({"detail": f"가계부 수정 실패: {str(e)}"})

def delete_wallet(user, wallet_uuid):
    try:
        wallet = Wallet.objects.get(user=user, wallet_uuid=wallet_uuid)

        wallet.delete()

        return wallet
    except Exception as e:
        print("💥 Wallet 삭제 오류:", e)
        raise ValidationError({"detail": f"삭제 실패: {str(e)}"})

def total_wallet(user, year, month):
    try:

        income = Wallet.objects.filter(user=user, date__year=year, date__month=month, type = 'INCOME')
        expense = Wallet.objects.filter(user=user, date__year=year, date__month=month, type = 'EXPENSE')

        total_income = income.aggregate(Sum('amount'))['amount__sum'] or int(0)

        total_expense = expense.aggregate(Sum('amount'))['amount__sum'] or int(0)

        print(total_income, total_expense)

        return {
            "total_income": total_income,
            "total_expense": total_expense
        }
    except Exception as e:
        print("💥 총합 계산 오류:", e)
        return  ValidationError({"detail": f"총합 계산 오류: {str(e)}"})

# 가계부 월별 리스트
def get_wallet_monthly(user, year, month):

    try:
        top_wallets = (Wallet.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        ).annotate(
            only_date=TruncDate('date')
        ).annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=[F('only_date')],
                order_by=[F('amount').desc(),
                          F('created_at').asc()
                ]
            )
        ).filter(row_number=1))

        # 날짜별 전체 amount 합계
        daily_sums = (
            Wallet.objects
            .filter(user=user, date__year=year, date__month=month)
            .annotate(only_date=TruncDate('date'))
            .values('only_date')
            .annotate(total=Sum('amount'))
        )

        # 날짜 → 합계 딕셔너리로 변환
        daily_sum_map = {row['only_date']: row['total'] for row in daily_sums}

        # 날짜 → top entry 매핑
        result_map = defaultdict(list)

        for wallet in top_wallets:

            result_map[wallet.only_date].append(
                    wallet_to_dict(wallet)
            )

        # 응답 구성
        first_day = date(year, month, 1)
        num_days = monthrange(year, month)[1]


        monthly = []

        for i in range(num_days):
            current_date = first_day + timedelta(days=i)
            entries = result_map.get(current_date, [])
            total_amount = daily_sum_map.get(current_date, 0)


            monthly.append({
                "date": current_date,
                "totalAmount": total_amount,
                "entries": entries
            })

        return {"monthly": monthly}

    except Exception as e:
        print("💥 Wallet 월별 조회 오류:", e)
        raise ValidationError({"detail": f"월별 조회 실패: {str(e)}"})

# 가계부 일별 리스트
def get_wallet_daily(user, date) :
    try:
        wallets = Wallet.objects.filter(user=user, date=date)

        result_map = defaultdict(list)


        for wallet in wallets :

            result_map[
                ㅔwallet.date.strftime("%Y-%m-%d") if isinstance(wallet.date, (date, datetime)) else wallet.date
            ].append(
                    wallet_to_dict(wallet)
            )

        return {"entries": result_map}
    except Exception as e:
        print("💥 Wallet 일별 조회 오류:", e)
        raise ValidationError({"detail": f"일별 조회 실패: {str(e)}"})

# 가계부 전체 리스트
def get_wallet_list(user, page, size, keyword):
    try:
        wallets = Wallet.objects.filter(user=user)

        if keyword:
            wallets = wallets.filter(
                Q(title__icontains=keyword) | Q(content__icontains=keyword)
            )

        wallets = wallets.order_by(F('created_at').desc())
        paginator = Paginator(wallets, size)
        page_obj = paginator.get_page(page)

        result = []

        for wallet in page_obj.object_list:
            result.append({
                # 딕셔너리 언패킹 (dictionary unpacking) 문법 dict 안에 또 다른 dict를 키-값
                **wallet_to_dict(wallet),
                "date": (
                    wallet.date.strftime("%Y-%m-%d")
                    if isinstance(wallet.date, (date, datetime))
                    else wallet.date
                )

            })

        return {"page": page_obj.number,
                "totalPages" : paginator.num_pages,
                "totalItems" : paginator.count,
                "result": result
        }

    except Exception as e:
        print("💥 Wallet 전체 조회 오류:", e)
        raise ValidationError({"detail": f"전체 조회 실패: {str(e)}"})

# 중복 코드
def wallet_to_dict(wallet):
    return {
        "walletUuid": str(wallet.wallet_uuid),
        "walletCategory": str(wallet.wallet_category),
        "title": wallet.title,
        "emotion": str(wallet.emotion),
        "type": str(wallet.type),
        "amount": int(wallet.amount)
}