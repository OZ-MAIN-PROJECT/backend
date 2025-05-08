from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from wallet import services
from wallet.serializers import WalletCreateSerializer, WalletDetailSerializer, WalletUpdateSerializer



# 가계부 생성
class WalletListCreateView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인 필수


    def post(self, request):



        serializer = WalletCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet = services.create_wallet(
            user = request.user,
            data=serializer.validated_data
        )


        return Response({"walletUuid": wallet.wallet_uuid}, status=201)

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not (year and month):
            return Response({"detail": "year와 month는 필수입니다."}, status=400)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({"detail": "year와 month는 숫자여야 합니다."}, status=400)

        result = services.get_wallet_monthly(
            user = request.user,
            year = year,
            month = month
        )

        return Response(result, status=200)

class WalletView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인 필수


    # 가계부 개별 조회
    def get(self, request, wallet_uuid):


        wallet = services.get_wallet_detail(
            user = request.user,
            wallet_uuid = wallet_uuid
        )

        serializer = WalletDetailSerializer(wallet)

        return Response(serializer.data, status=200)

    # 가계부 수정
    def patch(self, request, wallet_uuid):

        serializer = WalletUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet = services.update_wallet(
            user = request.user,
            wallet_uuid = wallet_uuid,
            data=serializer.validated_data
        )

        return Response({"walletUuid": wallet.wallet_uuid}, status=200)

    def delete(self, request, wallet_uuid):

        services.delete_wallet(
            user = request.user,
            wallet_uuid = wallet_uuid
        )

        return Response(status=204)


class WalletTotalView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인 필수


    def get(self, request):

        year = request.query_params.get('year')
        month = request.query_params.get('month')


        if not (year and month):
            return Response({"detail": "year와 month는 필수입니다."}, status=400)


        result = services.total_wallet(
            user = request.user,
            year = year,
            month = month
        )


        return Response({"income": result["total_income"],
                         "expense" : result["total_expense"]}, status=200)


class WalletDailyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date = request.query_params.get('date')

        if not date:
            return Response({"detail": "year와 month는 필수입니다."}, status=400)


        result = services.get_wallet_daily(
            user = request.user,
            date = date
        )

        return Response(result, status=200)