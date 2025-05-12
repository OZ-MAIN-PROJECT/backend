from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from statistic import services


class WalletEmotionStatisticView(APIView):
    permission_classes = [IsAuthenticated]

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

        result = services.get_emotion_statistic(
            user = request.user,
            year = year,
            month = month
        )

        return Response(result, status=200)