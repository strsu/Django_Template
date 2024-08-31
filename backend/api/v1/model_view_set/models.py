from django.db import models, transaction, connection
from django.db.models import Prefetch
from django.db.utils import OperationalError
from django.core.cache import cache

from api.v1.user.models import User

import time


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

    @classmethod
    def get_product_with_order_list(cls):
        """
            to_attr 을 넣으면 
                1. Prefetch 한 productorder_set 의 이름을 바꿀 수 있다.
                2. list로 넘어오기 때문에 객체가 아닌 value의 형태로 자동변환된다.
            order for문을 수행할 때 추가적인 쿼리가 실행되지 않는다.
        """
        products = Product.objects.all().prefetch_related(
            Prefetch(
                "productorder_set", queryset=ProductOrder.objects.all(), to_attr="product_order"
            )
        )

        for product in products:
            print(product.name, len(product.product_order))
            for order in product.product_order:
                print(order)

    @classmethod
    def get_product_with_order_orm(cls):
        """
            to_attr 을 안 넣으면 
                1. queryset으로 넘어오기 때문에 추가적인 orm 작업을 할 수 있다.
                2. 아래처럼 all()로 안하면 이터레이션이 안 됨.
            order for문을 수행할 때 추가적인 쿼리가 실행되지 않는다.
                -> queryset임에도 추가적인 쿼리 없음 (신기방기)
        """
        products = Product.objects.all().prefetch_related(
            Prefetch("productorder_set", queryset=ProductOrder.objects.all())
        )

        for product in products:
            print(product.name, product.productorder_set.all().count())
            for order in product.productorder_set.all():
                print(order)

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
        try:
            with transaction.atomic():
                locked_product = Product.objects.select_for_update().get(id=product)
                if locked_product.remaining_items >= amount:
                    locked_product.remaining_items -= amount
                    locked_product.save()
                    ProductOrder.objects.create(
                        product=locked_product, purchaser=purchaser, amount=amount
                    )
                else:
                    raise Exception("현재 남은 상품이 부족합니다.")
        except Product.DoesNotExist:
            raise Exception("상품정보를 찾을 수 없습니다.")
        except OperationalError:
            raise Exception("주문실패, 다시 시도해주세요.")
        except Exception as e:
            raise Exception(e)

    @classmethod
    def purchase_by_cache(cls, product, purchaser, amount):
        """
        주문자의 이중결제를 방지하기 위해서 `상품ID:주문자ID` 로 cache key를 생성한다.
        이렇게 하면
            * 주문자 이중결제는 Application Lock으로 예방
            * 상품의 개수 부족은 DB Lock으로 해결한다
        """
        product_reserve_key = f"product_reserve_key:{product}:{purchaser.uuid}"

        """
        Cache Lock을 함께 사용하면 데이터베이스 트랜잭션 이전에 애플리케이션 레벨에서 중복 작업을 더 빨리 차단할 수 있다. 
        이렇게 하면 동시성 문제에 대한 추가적인 안전장치를 마련하게 된다.

        Cache Lock을 사용하면 nowait=True 를 설정하지 않아도 나중에 온 요청에 대해 Exception이 발생한다.

        *** Redis NX ***
        NX 옵션을 전달하면 SET 하려는 키가 없는 경우에만 SET이 성공한다. 
        Redis는 싱글 스레드로 동작하기 때문에 여러 프로세스가 공유 자원에 접근할 때 발생하는 동시성 문제를 이 명령어로 해결할 수 있다.
        즉 먼저 접근한 쓰레드가 NX 옵션을 전달한 SET에 성공한다면 다른 쓰레드들은 대기한다. 
        여기서 다른 쓰레드들이 대기하도록 while 문과 같은 루프와 Sleep같은 함수는 개발자가 직접 제공해야 한다.
        """
        # 캐시 키가 존재하지 않을 때만 키를 설정하고, 설정에 성공하면 True 반환
        if cache.set(
            product_reserve_key, "1", nx=True, timeout=5
        ):  # 5초 동안 잠금 유지, 실수로 캐시가 안 지워져도 5초 뒤에는 지워질 수 있도록!

            try:
                """
                    with transaction.atomic()
                    내부에서 try except는 권장하지 않는다!!
                    왜???
                    안에서 exception 처리하다가 실수하면 rollback이 안될 수 있어서!
                """
                with transaction.atomic():
                    locked_product = Product.objects.select_for_update().get(id=product)
                    if locked_product.remaining_items >= amount:
                        locked_product.remaining_items -= amount
                        locked_product.save()
                        ProductOrder.objects.create(
                            product=locked_product, purchaser=purchaser, amount=amount
                        )
                    else:
                        raise ValueError("현재 남은 상품이 부족합니다.")
            except Product.DoesNotExist:
                raise ValueError("상품정보를 찾을 수 없습니다.")
            except OperationalError:
                raise ValueError("주문실패, 다시 시도해주세요.")
            except Exception as e:
                raise ValueError(e)
            finally:
                # 어떤 Exception이 터지든 로직이 끝나면 캐시는 비워야 한다.
                cache.delete(product_reserve_key)
        else:
            # 이미 다른 프로세스가 예약 중이므로 적절한 응답을 반환
            raise ValueError("주문실패, 다시 시도해주세요.")

    @classmethod
    def purchase_with_retry(cls, product, purchaser, amount):
        for attempt in range(3):  # 3번의 재시도
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SET LOCAL statement_timeout = 5000;"
                    )  # 5초로 타임아웃 설정

                    with transaction.atomic():
                        locked_product = Product.objects.select_for_update().get(
                            id=product
                        )

                        if locked_product.remaining_items >= amount:
                            locked_product.remaining_items -= amount
                            locked_product.save()

                            ProductOrder.objects.create(
                                product=locked_product,
                                purchaser=purchaser,
                                amount=amount,
                            )
                        else:
                            raise Exception("현재 남은 상품이 부족합니다.")

                # 성공적으로 끝났다면 루프 종료
                return "구매 성공"

            except OperationalError:
                # 재시도 전에 잠시 대기
                if attempt < 2:
                    time.sleep(1)
                else:
                    raise Exception("주문 실패, 다시 시도해주세요.")
            except Product.DoesNotExist:
                raise Exception("상품 정보를 찾을 수 없습니다.")
            except Exception as e:
                raise Exception(str(e))

    class Meta:
        db_table = "product_order"
        verbose_name = "상품 주문"
        verbose_name_plural = "상품 주문"
