from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class EmotionChoices(models.TextChoices):
    HAPPY = 'happy', '행복'
    SAD = 'sad', '슬픔'
    ANGRY = 'angry', '분노'
    ANXIOUS = 'anxious', '불안'
    COMFORT = 'comfort', '위로'
    SATISFIED = 'satisfied', '만족'
    TIRED = 'tired', '지침'
    EXPECTED = 'expected', '기대'

class WalletEmotion(models.Model):
    wallet_emotion_type = models.CharField(max_length=60, primary_key=True)  # ex: 'happy'
    wallet_emotion_id = models.PositiveIntegerField(unique=True)

    class Meta:
        db_table = 'wallet_emotion'

    def __str__(self):
        return self.emotion_type


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

class WalletCategory(models.Model):
    wallet_category_type = models.CharField(max_length=60, primary_key=True)  # ex: 'food'
    wallet_category_id = models.PositiveIntegerField(unique=True)

    class Meta:
        db_table = 'wallet_category'

    def __str__(self):
        return self.wallet_category_type



class Wallet(models.Model):
    TYPE_CHOICES = [
        ('Expense', '지출'),
        ('Income', '수입'),
    ]


    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    type = models.CharField(max_length=40, choices=TYPE_CHOICES)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    balance = models.DecimalField(decimal_places=2, max_digits=10)
    title = models.CharField(max_length=255)
    content = models.TextField()
    wallet_category = models.ForeignKey(WalletCategory, to_field='wallet_category_type', on_delete=models.PROTECT, null=False)
    emotion = models.ForeignKey(WalletEmotion, to_field='wallet_emotion_type', on_delete=models.PROTECT, null=False)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        db_table = 'wallet'
