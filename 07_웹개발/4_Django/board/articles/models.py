from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  # django default user model


# CASCADE : 폭포
# on_delete : CASCADE 게시물이 삭제되면 폭포처럼 댓글도 다 지워버린다.
class Article(models.Model):
    date = models.DateTimeField()  # 작성 날짜 시간
    title = models.CharField(max_length=100)  # 글자수 제한
    content = models.TextField()  # 글자수 제한 없음
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User Foreign key


class Comment(models.Model):
    date = models.DateTimeField()   # 날짜
    content = models.TextField()  # 댓글
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  # Article  Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User Foreign key


