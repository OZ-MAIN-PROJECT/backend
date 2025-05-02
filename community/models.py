from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# 커뮤니티 카테고리
class CommunityCategory(models.Model):
    community_category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'community_category'

    def __str__(self):
        return self.name


# 커뮤니티 게시글
class Community(models.Model):
    COMMUNITY_TYPE_CHOICES = [
        ('QNA', '질문 게시판'),
        ('INFORMATION', '감정 소비 이야기'),
        ('NOTICE', '공지사항'),
    ]

    community_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community_category = models.ForeignKey(CommunityCategory, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=20, choices=COMMUNITY_TYPE_CHOICES)
    title = models.CharField(max_length=100)
    content = models.TextField()
    like_count = models.PositiveIntegerField(default=0) # 좋아요 수
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'community'

    def __str__(self):
        return self.title


# 커뮤니티 댓글/대댓글
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies') # 대댓글일 경우 연결된 부모 댓글
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return f"{self.user} : {self.content}"


# 좋아요 기록
class CommunityLike(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'community')  # 중복으로 좋아요 불가
        db_table = 'community_like'

    def __str__(self):
        return f"{self.user} likes {self.community}"
    
# 조회수 기록
class CommunityView(models.Model):
    view_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_togeter = ('user', 'community') # 중복으로 조회수 카운트 불가
        db_table = 'community_view'

    def __str__(self):
        return f"{self.user} viewed {self.community}"
