from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# 공지사항 게시글
class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 관리자
    title = models.CharField(max_length=100)
    content = models.TextField()
    like_count = models.PositiveIntegerField(default=0)  # 좋아요 수
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notice'

    def __str__(self):
        return self.title


# 공지사항 좋아요
class NoticeLike(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notice_like'
        constraints = [
            models.UniqueConstraint(fields=['user', 'notice'], name='unique_user_notice_like')
        ]

    def __str__(self):
        return f"{self.user} likes notice {self.notice}"


# 공지사항 조회수
class NoticeView(models.Model):
    view_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='views')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notice_view'
        constraints = [
            models.UniqueConstraint(fields=['user', 'notice'], name='unique_user_notice_view')
        ]

    def __str__(self):
        return f"{self.user} viewed notice {self.notice}"