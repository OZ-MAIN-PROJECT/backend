from django.urls import path

from statistic.views import WalletEmotionStatisticView

urlpatterns = [

    path("emotion/",WalletEmotionStatisticView.as_view(), name="emotion"),
]