from django.db import models
from django.db.models import Q

from api.common.models import TimestampModel
from api.common.utils import kst_to_unixtime, unixtime_to_kst, now_unixtime

from django.contrib.auth import get_user_model

from config.exceptions.custom_exceptions import CustomException

from datetime import datetime
import time


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "goods/owner_{0}/{1}".format(instance.owner.uuid, filename)


class Goods(TimestampModel):

    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="소유자",
    )

    title = models.CharField("제목", max_length=256)
    content = models.TextField("상세내용")
    image = models.ImageField(upload_to=user_directory_path)

    @classmethod
    def get_goods(cls, **kwargs) -> "Goods":
        try:
            obj = Goods.actives.get(**kwargs)
        except Goods.DoesNotExist:
            raise CustomException(detail="상품을 찾을 수 없습니다", code=404)
        else:
            return obj

    class Meta:
        verbose_name = "상품"
        verbose_name_plural = "상품"


class GoodsBuyer(TimestampModel):

    goods = models.ForeignKey(
        verbose_name="상품",
        to=Goods,
        on_delete=models.DO_NOTHING,
    )
    buyer = models.ForeignKey(
        verbose_name="빌리는사람",
        to=get_user_model(),
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = "구매자"
        verbose_name_plural = "구매자"


class GoodsChatRoom(TimestampModel):
    product = models.ForeignKey(
        verbose_name="상품",
        to=Goods,
        on_delete=models.DO_NOTHING,
    )
    buyer = models.ForeignKey(
        verbose_name="회원",
        to=get_user_model(),
        on_delete=models.DO_NOTHING,
    )

    owner_last_read_at = models.DateTimeField("마지막 읽은 시각", null=True)
    buyer_last_read_at = models.DateTimeField("마지막 읽은 시각", null=True)

    @classmethod
    def get_rooms(cls, user):
        return cls.actives.select_related("product").filter(Q(product__owner=user) | Q(buyer=user))

    def get_messages(self, timestamp: datetime | None, cnt=100):
        if timestamp is None:
            timestamp = int(time.time() * 1000)
        else:
            timestamp = kst_to_unixtime(timestamp)

        if self.goodschatconversation_set:
            return self.goodschatconversation_set.all()[:cnt]

        return GoodsChatConversation.objects.filter(room=self, timestamp__lte=timestamp).order_by("-timestamp")[:cnt]

    def save(self, *args, **kwargs):
        try:
            if self.buyer == self.product.owner:
                raise CustomException(detail="자신과의 채팅방은 생성할 수 없습니다", code=400)
        except Goods.DoesNotExist:
            raise CustomException(detail="상품을 찾을 수 없습니다", code=404)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "채팅방"
        verbose_name_plural = "채팅방"


class GoodsChatConversation(models.Model):
    class MessageType(models.IntegerChoices):
        TEXT = 1, "메세지"
        IMAGE = 2, "이미지"

    room = models.ForeignKey(
        verbose_name="채팅방",
        to=GoodsChatRoom,
        on_delete=models.DO_NOTHING,
    )

    # Unix 타임스탬프 (밀리초 단위)
    timestamp = models.BigIntegerField("보낸시각", blank=True, null=True)
    type = models.IntegerField("메시지 종류", choices=MessageType.choices)
    message = models.CharField("메세지 내용", max_length=256)
    is_guest = models.BooleanField("guest", default=False)

    def get_kst(self):
        return unixtime_to_kst(self.timestamp / 1000)

    def get_message(self):
        if self.type == GoodsChatConversation.MessageType.TEXT:
            return self.message
        return "이미지"

    def save(self, sender=None, *args, **kwargs):
        if sender is not None:
            self.is_guest = sender == self.room.buyer
        # 메시지를 저장할 때 타임스탬프를 현재 밀리초 단위로 설정
        if self.timestamp is None:
            self.timestamp = now_unixtime()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "채팅내용"
        verbose_name_plural = "채팅내용"

        indexes = [
            models.Index(fields=["room", "timestamp"]),
        ]
