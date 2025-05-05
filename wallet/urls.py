from django.urls import path
from wallet.views import WalletCreateView

urlpatterns = [

    path("", WalletCreateView.as_view(), name="wallet_create"),
]