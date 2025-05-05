from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TypeChoices(models.TextChoices):
    EXPENSE = 'Expense', '지출'
    INCOME = 'Income', '수입'

class EmotionChoices(models.TextChoices):
    HAPPY = 'happy', '행복'
    SAD = 'sad', '슬픔'
    ANGRY = 'angry', '분노'
    ANXIOUS = 'anxious', '불안'
    COMFORT = 'comfort', '위로'
    SATISFIED = 'satisfied', '만족'
    TIRED = 'tired', '지침'
    EXPECTED = 'expected', '기대'

class WalletCategoryChoices(models.TextChoices):
    FOOD = 'food', '식비'
    LIVING = 'living', '생활'
    TRANSPORT = 'transport', '교통/차량'
    HEALTH = 'health', '건강'
    EDUCATION = 'education', '교육'
    SHOPPING = 'shopping', '쇼핑'
    CULTURE = 'culture', '여가/문화'
    FINANCE = 'finance', '금융'

    SALARY = 'salary', '급여'
    BONUS = 'bonus', '상여/보너스'
    POCKET_MONEY = 'pocket_money', '용돈'
    SIDE_JOB = 'side_job', '부수입'
    INVESTMENT = 'investment', '투자 수익'
    REFUND = 'refund', '환급'


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    type = models.CharField(max_length=10, choices=TypeChoices.choices)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    balance = models.DecimalField(decimal_places=2, max_digits=10)
    title = models.CharField(max_length=255)
    content = models.TextField()
    wallet_category = models.CharField(max_length=30, choices=WalletCategoryChoices.choices)
    emotion = models.CharField(max_length=20, choices=EmotionChoices.choices)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)