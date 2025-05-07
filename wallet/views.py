from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from statistic.models import MonthlyStatistic
from wallet import services
from wallet.serializers import WalletCreateSerializer, WalletDetailSerializer, WalletUpdateSerializer

# 로그인이 안되서 유저 지정(테스트를 위해 나중에 지워야함)
# User = get_user_model()
# user = User.objects.first()

# 가계부 생성
class WalletCreateView(APIView):
    # permission_classes = [IsAuthenticated]  # 로그인 필수
    permission_classes = [AllowAny] # 나중에 bearer Token 받을 수 있으면 삭제


    def post(self, request):

        # 로그인이 안되서 유저 지정(테스트를 위해 나중에 지워야함)
       # test_user = User.objects.first()

        serializer = WalletCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet = services.create_wallet(
            user = request.user,
            data=serializer.validated_data
        )


        return Response({"walletUuid": wallet.wallet_uuid}, status=201)


class WalletView(APIView):
    permission_classes = []

    # 가계부 개별 조회
    def get(self, request, wallet_uuid):
       # test_user = User.objects.first()

        wallet = services.get_wallet_detail(
            user = request.user,
            wallet_uuid = wallet_uuid
        )

        serializer = WalletDetailSerializer(wallet)

        return Response(serializer.data, status=200)

    # 가계부 수정
    def patch(self, request, wallet_uuid):
        # test_user = User.objects.first()

        serializer = WalletUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet = services.update_wallet(
            user = request.user,
            wallet_uuid = wallet_uuid,
            data=serializer.validated_data
        )

        return Response({"walletUuid": wallet.wallet_uuid}, status=200)

    def delete(self, request, wallet_uuid):
        # test_user = User.objects.first()

        services.delete_wallet(
            user = request.user,
            wallet_uuid = wallet_uuid
        )

        return Response(status=204)


class WalletTotalView(APIView):
    permission_classes = []
    def get(self, request):

        year = request.query_params.get('year')
        month = request.query_params.get('month')

        # test_user = User.objects.first()

        if not (year and month):
            return Response({"detail": "year와 month는 필수입니다."}, status=400)


        result = services.total_wallet(
            user = request.user,
            year = year,
            month = month
        )


        return Response({"income": result["total_income"],
                         "expense" : result["total_expense"]}, status=200)
