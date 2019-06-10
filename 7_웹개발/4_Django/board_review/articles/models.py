from django.db import models


class Articles(models.Model):
    title = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    date = models.DateTimeField()
    content = models.TextField()


