from django.db import models
from api.v1.user.models import User

# Create your models here.
class File(models.Model):

    date = models.DateTimeField("등록일", auto_now_add=True)
    path = models.TextField("파일 경로", null=True)
    name = models.TextField("파일 명", null=True)
    code = models.TextField("코드", null=True)

    class Meta:
        verbose_name = "file"
