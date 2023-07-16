from django.db import models


# Create your models here.
class LogModel(models.Model):
    created_at = models.DateTimeField("생성일", auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField("수정일", auto_now=True, blank=True, null=True)
    deleted_at = models.DateTimeField("삭제일", blank=True, null=True)

    class Meta:
        abstract = True
