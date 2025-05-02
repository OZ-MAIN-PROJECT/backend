from django.db import models

class Community(models.Model):
    TYPE_CHOICES = [
        ("information", "정보"),
        ("qna", "질문"),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return f"[{self.type}] {self.title}"


class CommunityType(models.TextChoices):
    INFORMATION = 'information', '정보'
    QNA         = 'qna',         '질문'