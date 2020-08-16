from django.db import models
from django.conf import settings

user = settings.AUTH_USER_MODEL


class Article(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date = models.DateTimeField()
    content = models.TextField()


class Comment(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.TextField()

