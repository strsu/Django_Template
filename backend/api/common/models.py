from django.db import models
from django.utils import timezone

from api.common.manager import ActiveManager


# Create your models here.
class TimestampModel(models.Model):
    created_at = models.DateTimeField(
        "생성일", auto_now_add=True, blank=True, null=True
    )
    modified_at = models.DateTimeField("수정일", auto_now=True, blank=True, null=True)
    deleted_at = models.DateTimeField("삭제일", blank=True, null=True)

    raw_objects = models.Manager()  # default manager
    actives = ActiveManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True
        default_manager_name = "raw_objects"  # 이걸 안 쓰면 TimestampModel을 상속받은 모델에서 새로운 manager를 할당하면 obejcts를 쓸 수 없게된다.


class ResponseModel(models.Model):

    request_at = models.DateTimeField(
        "생성일", auto_now_add=True, blank=True, null=True
    )

    uri = models.CharField("주소", max_length=255)
    query_param = models.TextField(null=True, blank=True)
    method = models.CharField("", max_length=10)
    status_code = models.SmallIntegerField("응답코드")
    response_time = models.FloatField("응답시간")

    class Meta:
        verbose_name = "응답"
        verbose_name_plural = "응답"
