import uuid
from django.db import models


class GenderChoices(models.TextChoices):
    MALE = 'M', '남성'
    FEMALE = 'F', '여성'
    OTHER = 'O', '기타'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

    gender = models.CharField(max_length=1, choices=GenderChoices.choices)

    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lastlogin_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.nickname
