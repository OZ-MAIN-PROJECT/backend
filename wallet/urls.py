from django.urls import path
from wallet.views import WalletListCreateView, WalletView, WalletTotalView, WalletDailyView, WalletListView

urlpatterns = [

    #POST /api/wallet 가계부 생성
    path("", WalletListCreateView.as_view(), name="wallet_create"),

    #GET /api/wallet/walletUuid 가계부 개별 상세 조회, 수정, 삭제
    path("<uuid:wallet_uuid>/", WalletView.as_view(), name="wallet_detail"),

    path("total", WalletTotalView.as_view(), name="wallet_total"),

    path("daily", WalletDailyView.as_view(), name="wallet_daily"),

    path("entries", WalletListView.as_view(), name="wallet_entries"),
]