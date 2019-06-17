from imagekit.models import ProcessedImageField
# https://github.com/matthewwithanm/django-imagekit
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.db import models


class Post(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_posts")  # 게시물을 좋아하는 사람들, M:N 관계
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    # image = models.ImageField(blank=True)  # allow null field
    image = ProcessedImageField(upload_to='posts/images',  # 올리는 위치 설정
                                processors=[ResizeToFill(600, 600)],
                                format='JPEG',
                                options={'quality': 80},
                                blank=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
