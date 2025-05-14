from django.urls import path

from statistic.views import WalletEmotionStatisticView, WalletCategoryStatisticView, WalletMonhtlyStatisticView

urlpatterns = [

    path("emotion/",WalletEmotionStatisticView.as_view(), name="emotion"),

    path("category/", WalletCategoryStatisticView.as_view(), name="category"),

    path("monthly/", WalletMonhtlyStatisticView.as_view(), name="monthly"),
]