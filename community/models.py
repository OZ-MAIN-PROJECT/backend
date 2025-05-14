from django.db import models

from users.models import User


class CommunityType(models.TextChoices):
    INFORMATION = 'information', '정보'
    QNA = 'qna', '질문'


class Community(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    type = models.CharField(max_length=20, choices=CommunityType.choices)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.type}] {self.title}"

class Comment(models.Model):
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()

    # parent가 None이면 최상위 댓글, 있으면 그 댓글의 대댓글
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return f"{self.user} on {self.community} – {self.content[:20]}"
