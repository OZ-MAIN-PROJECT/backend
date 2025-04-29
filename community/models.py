from django.db import models


class Information(models.Model):
    TYPE_CHOICES = [
        ('information', '정보 게시판'),
    ]
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='information')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    TYPE_CHOICES = [
        ('qna', '질문 게시판'),
    ]
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='qna')
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_resolved = models.BooleanField(default=False)  # 질문 해결 여부
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Notice(models.Model):
    TYPE_CHOICES = [
        ('notice', '공지사항'),
    ]
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='notice')
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)  # 상단 고정 여부
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
