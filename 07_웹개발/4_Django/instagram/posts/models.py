# https://github.com/matthewwithanm/django-imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.db import models


class HashTag(models.Model):
    # unique=True: 고유한 값만 들어갈 수 있도록 함, 같은 내용은 id가 같다.
    content = models.CharField(max_length=50, unique=True)

    # 오브젝트 출력시 content 출력
    def __str__(self):
        return self.content


class Post(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_posts")  # 게시물을 좋아하는 사람들, M:N 관계
    hash_tags = models.ManyToManyField(HashTag, blank=True, related_name='post_tagged')  # 해시태그
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
