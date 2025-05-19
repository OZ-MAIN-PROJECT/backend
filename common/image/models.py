from django.db import models

from users.models import User

class RefType(models.TextChoices):
    EMOTION = 'EMOTION', '감정 소통'
    QUESTION = 'QUESTION', '질문'
    NOTICE = 'NOTICE', '공지 사항'


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    ref_type = models.CharField(max_length=20, choices=RefType.choices)
    ref_id = models.IntegerField(db_column='ref_id')
    url = models.URLField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'image'
