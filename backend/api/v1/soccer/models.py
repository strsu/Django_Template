from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import BadRequest
from django.db import models

from api.common.models import TimestampModel

from django.contrib.auth import get_user_model
from api.v1.history.models import TrackedModel

from datetime import datetime

from config.exceptions.custom_exceptions import Code400Exception


class SoccerPlace(models.Model):
    """
    장소를 따로 기록하면 나중에 사람들이 많이 가는, 추천할 수 있는? 기능이..
    """

    name = models.CharField("장소", max_length=30, blank=True, null=True)
    address = models.CharField("주소", max_length=100, blank=True, null=True)
    latitude = models.FloatField("위도", blank=True, null=True)
    longitude = models.FloatField("경도", blank=True, null=True)

    def save(self, *args, **kwargs):
        ## 할 일 정의
        if self.pk:
            ## NOTE - 내가 만든 Code400Exception 같은 Exception은 django에서 500으로 인지하기 때문에 Handler400을 사용하려면 django에서 만든 400 Exception을 사용해야한다.
            raise Code400Exception("수정금지")

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-"

    class Meta:
        db_table = "soccer_place"
        verbose_name_plural = "축구 장소"
        unique_together = (("latitude", "longitude"),)


class Soccer(TrackedModel, TimestampModel):
    class Level(models.IntegerChoices):
        RED = 1
        ORANGE = 2
        YELLO = 3
        GREEN = 4
        BLUE = 5
        INDIGO = 6
        PURPLE = 7
        BLACK = 8
        WHITE = 9
        GRAY = 10

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="사용자 id",
    )
    where = models.ForeignKey(
        SoccerPlace,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="soccer_place",
        verbose_name="place id",
    )

    when = models.DateField("언제", blank=True, null=True)
    level = models.IntegerField(
        "레벨", choices=Level.choices, default=Level.RED, blank=True, null=True
    )
    score = models.FloatField("내 점수", blank=True, null=True)
    memo = models.CharField("메모", max_length=100, blank=True, null=True)
    picture = ArrayField(
        models.CharField("사진명", max_length=100), blank=True, null=True
    )
    video = ArrayField(
        models.CharField("비디오명", max_length=100), blank=True, null=True
    )
    tags = ArrayField(
        models.CharField("태그", max_length=20), blank=True, null=True
    )  # 이건 혹시 나중에 공유하기 생기거나 태그별로 모아보기 있으면 좋을 것 같아서,,

    def save(self, *args, **kwargs):
        ## 할 일 정의
        super(Soccer, self).save(*args, **kwargs)

    def delete(self):
        self.deleted_at = datetime.now()

    class Meta:
        db_table = "soccer"
        verbose_name = "축구 기록"
        verbose_name_plural = "축구 기록"


class SoccerTime(models.Model):
    """
    1. 내가 총 운동한 시간
    2. 전체 순위 / 친구 순위 등 운동 시간 비교 등등
    -> 하면 어떨까
    --> 굳이 나눠야 하나 싶기도??
    """

    soccer = models.ForeignKey(
        Soccer,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="soccer_time",
        verbose_name="soccer id",
    )
    time_from = models.TimeField("시작 시간", blank=True, null=True)
    time_to = models.TimeField("종료 시간", blank=True, null=True)
    soccer_time = models.TimeField(
        "운동 시간 = 종료시간 - 시간시작", blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if self.time_from and self.time_to:
            date_from = datetime.combine(
                datetime.today(),
                datetime.strptime(str(self.time_from), "%H:%M:%S").time(),
            )
            date_to = datetime.combine(
                datetime.today(),
                datetime.strptime(str(self.time_to), "%H:%M:%S").time(),
            )
            self.soccer_time = str(date_to - date_from)

        super().save(*args, **kwargs)

    class Meta:
        db_table = "soccer_time"
        verbose_name_plural = "축구 시간"


class SoccerWith(models.Model):
    """
    1. 어디서, 누구와 함께
    -> 양방향 추가
    --> 하나만 할까 싶기도
    """

    user_from = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="with_user_from",
        verbose_name="사용자 id",
    )

    user_to = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="with_user_to",
        verbose_name="사용자 id",
    )

    soccer = models.ForeignKey(
        Soccer,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="soccer_with",
        verbose_name="soccer id",
    )

    class Meta:
        db_table = "soccer_with"
        verbose_name_plural = "축구 함께"
        unique_together = [["user_from", "user_to", "soccer"]]
