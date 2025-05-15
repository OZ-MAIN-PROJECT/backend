from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from statistic.services import create_monthly_statistic

User = get_user_model()

class Command(BaseCommand):
    help = '월별 통계 저장'

    def handle(self, *args, **options):
        today = datetime.today()
        last_month = today.replace(day=1) - timedelta(days=1)

        year = last_month.year
        month = last_month.month

        for user in User.objects.all():
            create_monthly_statistic(user, year, month)
            self.stdout.write(f"{user.email}: {year}-{month} 저장 완료")