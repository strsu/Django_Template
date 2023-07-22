from django.db import models

from api.v1.user.models import User

from functools import wraps
import json


def get_authenticated_user(func):
    @wraps(
        func,
    )
    def inner(request, *args, **kwargs):
        user = request.user

        # 모든 모델에 사용자 정보를 전달합니다.
        kwargs["user"] = user

        return func(request, *args, **kwargs)

    return inner


class History(models.Model):
    table_name = models.CharField(max_length=64, null=True, blank=True)
    verbose_name = models.CharField(max_length=64, null=True, blank=True)

    history = models.JSONField("변경기록", default=dict, null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="사용자 id",
    )

    class Meta:
        db_table = "history"
        verbose_name = "모델 변경 기록"


class TrackedModel(models.Model):
    class Meta:
        abstract = True

    log = {}

    def __init__(self, *args, **kwargs):
        super(TrackedModel, self).__init__(*args, **kwargs)
        for field in self._meta.get_fields():
            if isinstance(field, models.Field):
                if hasattr(self, field.name):
                    self.log[field.name] = {
                        "verbose_name": field.verbose_name,
                        "old": getattr(self, field.name),
                    }

    @get_authenticated_user
    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        for field in self._meta.get_fields():
            if isinstance(field, models.Field):
                if hasattr(self, field.name):
                    self.log[field.name]["new"] = getattr(self, field.name)

        changed_log = {}

        for key, logs in self.log.items():
            if "old" not in logs and "new" not in logs:
                continue
            if logs["old"] != logs["new"]:
                changed_log[key] = str(logs)

        if changed_log:
            db_table = self._meta.db_table
            model_name = self._meta.model_name
            verbose_name = self._meta.verbose_name
            history = History.objects.create(
                table_name=db_table,
                verbose_name=verbose_name,
                history=changed_log,
                user=user,
            )
            history.save()

        super(TrackedModel, self).save(*args, **kwargs)
