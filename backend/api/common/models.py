from django.db import models

from api.common.manager import ActiveManager


# Create your models here.
class TimestampModel(models.Model):
    created_at = models.DateTimeField("생성일", auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField("수정일", auto_now=True, blank=True, null=True)
    deleted_at = models.DateTimeField("삭제일", blank=True, null=True)

    objects = models.Manager()  # default manager
    actives = ActiveManager()

    class Meta:
        abstract = True
        default_manager_name = "objects"  # 이걸 안 쓰면 TimestampModel을 상속받은 모델에서 새로운 manager를 할당하면 obejcts를 쓸 수 없게된다.
