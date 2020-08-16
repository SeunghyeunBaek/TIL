from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.db import models


class User(AbstractUser):
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='follower')
    introduce = models.TextField(blank=True)
    image = ProcessedImageField(upload_to='accounts/images',  # 올리는 위치 설정
                                processors=[ResizeToFill(200, 200)],
                                format='JPEG',
                                options={'quality': 80},
                                blank=True)
