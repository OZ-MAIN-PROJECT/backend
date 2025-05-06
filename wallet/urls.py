from django.urls import path
from wallet.views import WalletCreateView, WalletView

urlpatterns = [

    #POST /api/wallet 가계부 생성
    path("", WalletCreateView.as_view(), name="wallet_create"),

    #GET /api/wallet/walletUuid 가계부 일별 조회
    path("<uuid:wallet_uuid>/", WalletView.as_view(), name="wallet_detail"),

]