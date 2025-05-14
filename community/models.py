from django.db import models

from users.models import User


class CommunityType(models.TextChoices):
    EMOTION = 'EMOTION', '감정 소통'
    QUESTION = 'QUESTION', '질문'


class Community(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    type = models.CharField(max_length=20, choices=CommunityType.choices)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"[{self.type}] {self.title}"

    class Meta:
        db_table = 'community'

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='comments',
        db_column='community_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        db_column='user_id'
    )
    content = models.TextField()

    # parent가 None이면 최상위 댓글, 있으면 그 댓글의 대댓글
    parentCommentId = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE,
        db_column='parent_comment_id'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def str(self):
        return f"{self.user} on {self.community} – {self.content[:20]}"

    class Meta:
        db_table = 'comment'