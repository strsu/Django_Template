from django.db import models, transaction, connection
from django.db.models import Prefetch
from django.db.utils import OperationalError, IntegrityError
from django.core.cache import cache

from django.contrib.auth import get_user_model

import time
import random


class ProductTag(models.Model):
    name = models.CharField("상품태그", max_length=64, unique=True)
    who = models.IntegerField("")

    @classmethod
    def get_tag_by_name(cls, name):
        """
        https://www.notion.so/youngjae-park/get_or_create-a820dec8614240fcaa73cf2900c64d31?pvs=4

        def get_or_create(self, defaults=None, **kwargs):
            try:
                return self.get(**kwargs), False
            except self.model.DoesNotExist:
                params = self._extract_model_params(defaults, **kwargs)
                # Try to create an object using passed params.
                try:
                    with transaction.atomic(using=self.db):
                        params = dict(resolve_callables(params))
                        return self.create(**params), True
                except IntegrityError:
                    try:
                        return self.get(**kwargs), False
                    except self.model.DoesNotExist:
                        pass
                    raise

        * model에 integrity 조건이 있다면
            이미 get_or_create 내부에서 atomic, integrity 검사를 하기 때문에 그냥 사용하면 된다.
            이렇게 하면 동시요청이 와도 둘 다 원하는 결과를 얻는다.
        * 하지만, integrity 조건이 없다면
            get_or_create로 동시요청 문제를 해결할 수 없다.

        """
        id = random.randint(1, 100000)

        # get_or_create 내부 구현체, 명시적 확인을 위한 코드
        # try:
        #     print(f"## try: {id}")
        #     return ProductTag.objects.get(name=name)
        # except ProductTag.DoesNotExist:
        #     print(f"## DoesNotExist: {id}")
        #     try:
        #         with transaction.atomic():
        #             print(f"## create: {id}")
        #             return ProductTag.objects.create(name=name, who=id)
        #     except IntegrityError:
        #         try:
        #             print(f"## IntegrityError: {id}")
        #             return ProductTag.objects.get(name=name)
        #         except ProductTag.DoesNotExist:
        #             pass
        #         raise

        tag, created = ProductTag.objects.get_or_create(name=name, defaults={"who": id})

        return tag

    class Meta:
        db_table = "product_tag"


class ProductType(models.Model):
    name = models.CharField("상품종류이름", max_length=64, unique=True)

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
    remaining_items = models.IntegerField("남은 물건 개수", null=False, blank=False, default=0)

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
                "productorder_set",
                queryset=ProductOrder.objects.all(),
                to_attr="product_order",
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

        1. Product.objects.all().prefetch_related(
            "productorder_set"
        )
        2. Product.objects.all().prefetch_related(
            Prefetch("productorder_set", queryset=ProductOrder.objects.all())
        )

        (1)은 모든 조작없이 product_order를 가져온다.
        (2)는 세부적인 조작을 수행하여필요한 product_order를 가져올 수 있다.
            -> queryset에 filter, order_by 등 각종 조건을 걸 수 있다.
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
        get_user_model(),
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
            select_for_update : transaction.atomic() 와 함께 사용해야 한다.
                -> 해당 행을 조회하면서 "쓰기 잠금"(write lock)을 걸어, 다른 트랜잭션이 해당 행을 수정할 수 없게 한다.
                @Param
                    nowait : default는 False로, False일 경우 row lock이 잡혀있다면 대기하고 True일 경우 에러를 발생시킨다.
                        -> 잠금을 얻을 수 없을 때 즉시 실패하고 django.db.utils.OperationalError 예외를 발생시킨다. 이는 잠금 대기 시간을 피하고자 할 때 유용할 수 있다.
                    skip_locked : default는 False로, True일 경우 조회한 데이터가 lock이 잡혀있다면 이를 무시한다.
                        -> 현재 다른 트랜잭션에 의해 잠긴 행을 건너뛰고, 잠금을 획득할 수 있는 행만 선택한다.
                    of : select_for_update 은 select_related와 같이 사용할 경우 join 한 테이블의 행도 함께 lock을 잡습니다. 이때 of를 사용하여 lock을 잡을 테이블을 명시할 수 있다.

            nowait
                True  : 2개 동시 요청이 올 시 1개는 Exception 발생
                False : 2개 동시 요청이 와도 Exception 발생 안 함, 1개 처리 후 나머지 1개 처리되는 것 같다.

        atomic으로 하지 않으면 최종적으로 남은 상품개수가 0개 이어도 주문한 상품개수는 기존 남은 상품개수를 넘어갈 수 있다.
        """

        try:
            with transaction.atomic():
                locked_product = Product.objects.select_for_update().get(id=product)
                if locked_product.remaining_items >= amount:
                    locked_product.remaining_items -= amount
                    locked_product.save()
                    ProductOrder.objects.create(product=locked_product, purchaser=purchaser, amount=amount)
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
                        ProductOrder.objects.create(product=locked_product, purchaser=purchaser, amount=amount)
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
                # NOTE -  transaction 안에 connection이 있어야 정상 동작한다!!! 반대면 동작 안한다!!
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.execute("SET LOCAL statement_timeout = 5000;")  # 5초로 타임아웃 설정

                        locked_product = Product.objects.select_for_update().get(id=product)

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

    @classmethod
    def purchase_with_retry_only_isolation(cls, product, purchaser, amount):
        """
        @SERIALIZABLE
            이렇게 하면 최종적으로 성공은 할 수 있다.
            그런데 retry가 충분히 커야 많은 요청에 대해 대비할 수 있다.
            문제는 요청이 언제 끝날지 모르는 단점이 있다.

        @REPEATABLE READ
            트랜잭션이 시작된 후 다른 트랜잭션이 데이터를 수정할 수 없도록 한다.
                -> 동시에 읽을 순 있지만, save할 때 왜 OperationlError 가 발생

            @ From postgresql doc
                they will only find target rows that were committed as of the transaction start time.
                    ->최초 트랜잭션 시작시 가져온 row를 찾는다.
                However, such a target row might have already been updated (or deleted or locked) by another concurrent transaction by the time it is found.
                In this case, the repeatable read transaction will wait for the first updating transaction to commit or roll back (if it is still in progress).
                    -> 만약 다른 트랜잭션에 의해서 데이터가 수정된 경우 업데이트를 기다리거나 롤백을 진행한다.
                    --> 아직까진 대기
                If the first updater rolls back, then its effects are negated and the repeatable read transaction can proceed with updating the originally found row.
                But if the first updater commits (and actually updated or deleted the row, not just locked it) then the repeatable read transaction will be rolled back with the message
                because a repeatable read transaction cannot modify or lock rows changed by other transactions after the repeatable read transaction began.
                    -> 여기서 다시 commit할 때 처음에 가져온 데이터랑 값이 다르면 변경할 수 없기 때문에 OperationlError를 발생시킨다!

                결론 : 동시에 볼 순 있지만, 데이터가 바뀌면 롤백이 일어나서 최종적으로 성공할 수 있다.

        """
        max_retry = 10
        for attempt in range(max_retry):
            is_error = False
            is_sold_out = False
            msg = None
            try:
                # NOTE -  transaction 안에 connection이 있어야 정상 동작한다!!! 반대면 동작 안한다!!
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        """
                        select_for_update는 Row에 대한 쓰기 잠금을 설정하지만, Isolation은 충돌에 대한 관리를 하기 때문에
                        격리수준을 변경하는것 만으로는 동시성 문제를 해결하기 어렵다!!

                            cursor.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
                                -> Dirty Read: 트랜잭션 1이 커밋되지 않은 데이터를 트랜잭션 2가 읽는 현상

                            cursor.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
                                -> Non-repeatable Read: 트랜잭션 중에 같은 데이터를 여러 번 읽을 때 값이 바뀌는 현상

                            cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
                                * NOTE - 트랜잭션이 시작된 후 다른 트랜잭션이 데이터를 수정할 수 없도록 합니다
                                * 한 트랜잭션 내에서는 항상 동일한 데이터를 읽는다.
                                * 재시도 과정은 트랜잭션 종료 후 다시 새로운 트랜잭션이기 때문에 변경된 데이터를 읽을 수 있다.
                                -> Phantom Read: 트랜잭션 중에 새로운 행이 삽입되었을 때 이전에 보지 못한 새로운 행을 읽는 현상

                            cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
                                -> 트랜잭션 1과 2가 동시에 실행되면 둘 중 하나에서 **OperationalError**가 발생
                        """
                        cursor.execute("SET LOCAL statement_timeout = 5000;")  # 5초로 타임아웃 설정
                        cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
                        # cursor.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")

                        locked_product = Product.objects.get(id=product)
                        print(
                            f"{purchaser.email}, attempt: {attempt}, remaining_items: {locked_product.remaining_items}"
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
                            is_sold_out = True
                            raise Exception("현재 남은 상품이 부족합니다.")

                # 성공적으로 끝났다면 루프 종료
                return "구매 성공"

            except OperationalError:
                is_error = True
                msg = "주문 실패, 다시 시도해주세요."
            except Product.DoesNotExist:
                is_error = True
                msg = "상품 정보를 찾을 수 없습니다."
            except Exception as e:
                is_error = True
                msg = str(e)
            finally:
                print(
                    f"{purchaser.email}, attempt: {attempt}, remaining_items: {locked_product.remaining_items}, {msg}"
                )
                if is_sold_out:
                    raise Exception(msg)

                if is_error:
                    if attempt > max_retry:
                        raise Exception(msg)

    class Meta:
        db_table = "product_order"
        verbose_name = "상품 주문"
        verbose_name_plural = "상품 주문"


class ProductCarrier(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    tracking_url = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "product_carrier"
        verbose_name = "상품 배송업체"
        verbose_name_plural = "상품 배송업체"


class ProductOrderShipping(models.Model):
    carrier = models.ForeignKey(ProductCarrier, on_delete=models.SET_NULL, null=True, related_name="shipments")
    product_order = models.OneToOneField(ProductOrder, on_delete=models.CASCADE, related_name="shipping")
    shipping_address = models.CharField(max_length=255)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    shipping_status = models.CharField(max_length=50)
    shipped_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "product_order_shipping"
        verbose_name = "상품 주문 배송지"
        verbose_name_plural = "상품 주문 배송지"


class Account(models.Model):

    customer = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
    )

    balance = models.FloatField("잔고", null=False, blank=False, default=0)

    @classmethod
    def deposit(cls, customer, deposit):
        account_key = f"account_deposit_key:{customer.uuid}"

        # 캐시 키가 존재하지 않을 때만 키를 설정하고, 설정에 성공하면 True 반환
        if cache.set(
            account_key, "1", nx=True, timeout=5
        ):  # 5초 동안 잠금 유지, 실수로 캐시가 안 지워져도 5초 뒤에는 지워질 수 있도록!

            try:
                with transaction.atomic():
                    locked_account = Account.objects.select_for_update().get(customer=customer)
                    locked_account.balance += deposit
                    locked_account.save()
            except Account.DoesNotExist:
                raise ValueError("고객의 계좌정보를 찾을 수 없습니다.")
            except OperationalError:
                raise ValueError("잠시 후 다시 시도해주세요")
            except Exception as e:
                raise ValueError(e)
            finally:
                # 어떤 Exception이 터지든 로직이 끝나면 캐시는 비워야 한다.
                cache.delete(account_key)
        else:
            # 이미 다른 프로세스가 예약 중이므로 적절한 응답을 반환
            raise ValueError("잠시 후 다시 시도해주세요")

    @classmethod
    def withdraw(cls, customer, withdraw):
        try:
            with transaction.atomic():
                locked_account = Account.objects.select_for_update().get(customer=customer)
                if locked_account.balance >= withdraw:
                    locked_account.balance -= withdraw
                    locked_account.save()
                else:
                    raise ValueError("잔액이 부족합니다.")
        except Account.DoesNotExist:
            raise ValueError("고객의 계좌정보를 찾을 수 없습니다.")
        except OperationalError:
            raise ValueError("잠시 후 다시 시도해주세요")
        except Exception as e:
            raise ValueError(e)

    class Meta:
        db_table = "customer_account"
        verbose_name = "계좌"
        verbose_name_plural = "계좌"
