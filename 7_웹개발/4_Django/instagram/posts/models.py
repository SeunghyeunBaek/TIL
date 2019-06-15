from django.db import models
# https://github.com/matthewwithanm/django-imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Post(models.Model):
    content = models.TextField()
    # image = models.ImageField(blank=True)  # allow null field
    image = ProcessedImageField(upload_to='posts/images',  # 올리는 위치 설정
                                processors=[ResizeToFill(600, 600)],
                                format='JPEG',
                                options={'quality': 80})
