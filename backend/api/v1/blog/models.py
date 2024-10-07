from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
    )
    date = models.DateTimeField("등록일")
    content = models.TextField("내용")
    tags = models.TextField("태그")

    class Meta:
        verbose_name = "blog"
