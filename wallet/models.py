import uuid

from django.db import models

from users.models import User


class EmotionChoices(models.TextChoices):
    HAPPY = '행복', '행복'
    SAD = '슬픔', '슬픔'
    ANGRY = '분노', '분노'
    ANXIOUS = '불안', '불안'
    COMFORT = '위로', '위로'
    SATISFIED = '만족', '만족'
    TIRED = '지침', '지침'
    EXPECTED = '기대', '기대'

class WalletEmotion(models.Model):
    wallet_emotion_type = models.CharField(max_length=60, primary_key=True)  # ex: 'happy'
    wallet_emotion_id = models.PositiveIntegerField(unique=True)

    class Meta:
        db_table = 'wallet_emotion'

    def __str__(self):
        return self.wallet_emotion_type


class WalletCategoryChoices(models.TextChoices):
    FOOD = '식비', '식비'
    LIVING = '생활', '생활'
    TRANSPORT = '교통/차량', '교통/차량'
    HEALTH = '건강', '건강'
    EDUCATION = '교육', '교육'
    SHOPPING = '쇼핑', '쇼핑'
    CULTURE = '여가/문화', '여가/문화'
    FINANCE = '금융', '금융'

    SALARY = '급여', '급여'
    BONUS = '상여/보너스', '상여/보너스'
    POCKET_MONEY = '용돈', '용돈'
    SIDE_JOB = '부수입', '부수입'
    INVESTMENT = '투자수익', '투자수익'
    REFUND = '환급', '환급'

class WalletCategory(models.Model):
    wallet_category_type = models.CharField(max_length=60, primary_key=True)  # ex: 'food'
    wallet_category_id = models.PositiveIntegerField(unique=True)

    class Meta:
        db_table = 'wallet_category'

    def __str__(self):
        return self.wallet_category_type



class Wallet(models.Model):
    TYPE_CHOICES = [
        ('EXPENSE', '지출'),
        ('INCOME', '수입'),
    ]


    id = models.AutoField(primary_key=True)
    wallet_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    type = models.CharField(max_length=40, choices=TYPE_CHOICES)
    amount = models.IntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    wallet_category = models.ForeignKey(WalletCategory, to_field='wallet_category_type', on_delete=models.PROTECT, null=False)
    emotion = models.ForeignKey(WalletEmotion, to_field='wallet_emotion_type', on_delete=models.PROTECT, null=False)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        db_table = 'wallet'
