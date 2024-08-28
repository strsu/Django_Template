from django.db import models, transaction
from django.db.utils import OperationalError

from api.v1.user.models import User


class ProductType(models.Model):
    name = models.CharField("상품종류이름", max_length=64)

    class Meta:
        db_table = "product_type"


class Product(models.Model):
    name = models.CharField("상품 이름", max_length=64)
    price = models.IntegerField("상품 가격")
    type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="type id",
    )
    memo = models.CharField("메모", max_length=256)
    remaining_items = models.IntegerField(
        "남은 물건 개수", null=False, blank=False, default=0
    )

    class Meta:
        db_table = "product"


class ProductOrder(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="product_id",
    )
    purchaser = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
    )

    amount = models.IntegerField("구매한 물건 개수", null=False, blank=False, default=0)

    @classmethod
    def purchase(cls, product, purchaser, amount):
        """
        ## Race Condition
            nowait : default는 False로, False일 경우 row lock이 잡혀있다면 대기하고 True일 경우 에러를 발생시킨다.
                -> 잠금을 얻을 수 없을 때 즉시 실패하고 django.db.utils.OperationalError 예외를 발생시킨다. 이는 잠금 대기 시간을 피하고자 할 때 유용할 수 있다.
            skip_locked : default는 False로, True일 경우 조회한 데이터가 lock이 잡혀있다면 이를 무시한다.
                -> 현재 다른 트랜잭션에 의해 잠긴 행을 건너뛰고, 잠금을 획득할 수 있는 행만 선택한다.
            of : select_for_update 은 select_related와 같이 사용할 경우 join 한 테이블의 행도 함께 lock을 잡습니다. 이때 of를 사용하여 lock을 잡을 테이블을 명시할 수 있다.

        select_for_update() 는 transaction.atomic() 와 함께 사용해야 한다.
        """
        """
            nowait 
                True  : 2개 동시 요청이 올 시 1개는 Exception 발생
                False : 2개 동시 요청이 와도 Exception 발생 안 함, 1개 처리 후 나머지 1개 처리되는 것 같다.

        """
        with transaction.atomic():
            try:
                locked_product = Product.objects.select_for_update().get(id=product)
            except Product.DoesNotExist:
                raise Exception("상품정보를 찾을 수 없습니다.")
            except OperationalError:
                raise Exception("주문실패, 다시 시도해주세요.")
            except Exception as e:
                raise Exception(e)
            else:
                if locked_product.remaining_items >= amount:
                    locked_product.remaining_items -= amount
                    locked_product.save()
                    ProductOrder.objects.create(
                        product=locked_product, purchaser=purchaser, amount=amount
                    )
                else:
                    raise Exception("현재 남은 상품이 부족합니다.")

    class Meta:
        db_table = "product_order"
        verbose_name = "상품 주문"
        verbose_name_plural = "상품 주문"
