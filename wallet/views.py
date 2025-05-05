from django.contrib.auth import get_user_model
from django.core.serializers import serialize
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from wallet import services
from wallet.serializers import WalletCreateSerializer

#로그인이 안되서 유저 지정(테스트를 위해 나중에 지워야함)
User = get_user_model()
user = User.objects.first()

class WalletCreateView(APIView):
    # permission_classes = [IsAuthenticated]  # 로그인 필수
    permission_classes = [AllowAny] #나중에 bearer Token 받을 수 있으면 삭제


    def post(self, request):

        # 로그인이 안되서 유저 지정(테스트를 위해 나중에 지워야함)
        test_user = User.objects.first()

        serializer = WalletCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet = services.create_wallet(
            user=test_user,
            data=serializer.validated_data
        )


        return Response({"walletId": wallet.id}, status=201)
