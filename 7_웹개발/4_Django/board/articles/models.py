from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100)  # 글자수 제한
    content = models.TextField()  # 글자수 제한 없음

