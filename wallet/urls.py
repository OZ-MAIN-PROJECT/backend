from django.urls import path
from wallet.views import WalletCreateView, WalletDetailView

urlpatterns = [

    path("", WalletCreateView.as_view(), name="wallet_create"),

    path("<uuid:wallet_uuid>/", WalletDetailView.as_view(), name="wallet_detail"),
]