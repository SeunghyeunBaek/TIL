from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100)  # 글자수 제한
    content = models.TextField()  # 글자수 제한 없음


# CASCADE : 폭포
# on_delete : CASCADE 게시물이 삭제되면 폭포처럼 댓글도 다 지워버린다.
class Comment(models.Model):
    content = models.TextField()  # 댓글
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  # Article Class Foreign Key


