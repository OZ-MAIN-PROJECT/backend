from django.db import models

from users.models import User


class MonthlyStatistic(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    total_expense = models.IntegerField()
    total_income = models.IntegerField()
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'monthly_statistic'

