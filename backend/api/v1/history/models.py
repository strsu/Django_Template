from django.db import models

from api.v1.user.models import User

from functools import wraps
import uuid


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


class ModelHistory(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="사용자 id",
    )
    modified_at = models.DateTimeField("수정일", auto_now=True, blank=True, null=True)

    class Meta:
        db_table = "model_history"
        verbose_name = "모델 변경 기록"


class ModelHistoryDetail(models.Model):
    table_name = models.CharField(max_length=64, null=True, blank=True)
    verbose_name = models.CharField(max_length=64, null=True, blank=True)

    history = models.JSONField("변경기록", default=dict, null=True, blank=True)
    model_history = models.ForeignKey(
        ModelHistory,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="히스토리 id",
    )

    class Meta:
        db_table = "model_history_detail"
        verbose_name = "모델 변경 기록"


class TrackedModel(models.Model):
    class Meta:
        abstract = True

    """
        클래스 변수로 쓰면 TrackedModel을 상속받는 모든 모델의 객체는
        아래 변수를 공유해서 사용한다는 사실을 잊으면 안된다.
    """
    log = {}
    uuid = None

    def __init__(self, *args, **kwargs):
        super(TrackedModel, self).__init__(*args, **kwargs)

        if self.uuid is None:
            # 하나의 API에서 변경되는 모델을 함께 찾기 위해서
            self.uuid = uuid.uuid4()

        # 만약 같은 model 객체를 여러번 호출한다면, 가장 처음으로 호출되는 값이 old로 남아야 한다.
        # 그래서 굳이 db_table을 한번 더 키로 넣음으로써 old를 지킬 수 있다.
        db_table = self._meta.db_table
        if db_table not in self.log:
            self.log[db_table] = {}

        for field in self._meta.get_fields():
            if isinstance(field, models.Field):
                if hasattr(self, field.name):
                    if field.name not in self.log[db_table]:
                        self.log[db_table][field.name] = {
                            "verbose_name": field.verbose_name,
                            "old": getattr(self, field.name),
                        }
                    # 이미 키가 있다면, 그건 old가 아니다

    @get_authenticated_user
    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        db_table = self._meta.db_table

        for field in self._meta.get_fields():
            if isinstance(field, models.Field):
                if hasattr(self, field.name):
                    # field.name이 있다는 것은 곧 init도 호출되었다는 이야기
                    self.log[db_table][field.name]["new"] = getattr(self, field.name)

        changed_log = {}

        for key, logs in self.log[db_table].items():
            if logs["old"] != logs["new"]:
                changed_log[key] = {
                    **logs,
                    "old": str(logs["old"]),
                    "new": str(logs["new"]),
                }

        if changed_log:
            model_name = self._meta.model_name
            verbose_name = self._meta.verbose_name

            try:
                model_history = ModelHistory.objects.get(uuid=self.uuid)
            except:
                model_history = ModelHistory.objects.create(uuid=self.uuid, user=user)

            history = ModelHistoryDetail.objects.create(
                model_history=model_history,
                table_name=db_table,
                verbose_name=verbose_name,
                history=changed_log,
            )
            history.save()

        super(TrackedModel, self).save(*args, **kwargs)
