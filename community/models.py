from django.db import models


class CommunityType(models.TextChoices):
    INFORMATION = 'information', '정보'
    QNA = 'qna', '질문'


class Community(models.Model):
    type = models.CharField(max_length=20, choices=CommunityType.choices)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.type}] {self.title}"
