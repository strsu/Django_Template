from django.db import transaction, connection
from django.test import TransactionTestCase

from django.contrib.auth import get_user_model
from api.v1.model_view_set.models import Product, ProductOrder, ProductType

from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# python manage.py test api.v1.model_view_set.tests.test_product
# python manage.py test api/v1/model_view_set/tests/
# python manage.py test api/v1/model_view_set/tests --settings='config.settings.test_real_db'


class ProductTest(TransactionTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def tearDown(self):
        pass

    def 상품_등록(self, name, price, count, type=None):
        return Product.objects.create(
            name=name, price=price, remaining_items=count, type=type
        )

    def 구매자_생성(self, count=1):
        self.user_list = []
        for i in range(count):
            self.user_list.append(get_user_model().objects.create(email=f"user_{i}"))

    def _test_상품_동시_구매(self):

        num_user = 10
        remain = 7
        product = self.상품_등록("물건", 1000, remain)
        self.구매자_생성(num_user)

        def purchase(arg):
            try:
                # ProductOrder.purchase(*arg)
                ProductOrder.purchase_with_retry_only_isolation(*arg)
                return True
            except Exception as e:
                print(f"### {e}")
                return False

        args_list = []
        for i in range(num_user):
            args_list.append(
                (
                    product.id,
                    self.user_list[i],
                    1,
                )
            )

        time.sleep(2)

        results = []

        with ThreadPoolExecutor(max_workers=num_user) as executor:
            futures = [executor.submit(purchase, arg) for arg in args_list]
            for future in as_completed(futures):
                result = future.result()
                if future.done():
                    results.append(result)
                else:
                    future.cancelled()

        print(Product.objects.get(id=product.id).__dict__)

        self.assertEqual(results.count(True), remain)

    def test_상품_동시_조회(self):

        cloth = ProductType.objects.create(name="옷")
        eletronics = ProductType.objects.create(name="전자제품")

        product_cnt = 5
        products = [
            self.상품_등록(f"물건_{1}", 1000, 1, cloth),
            self.상품_등록(f"물건_{2}", 1000, 1, cloth),
            self.상품_등록(f"물건_{3}", 1000, 1, eletronics),
            self.상품_등록(f"물건_{4}", 1000, 1, eletronics),
            self.상품_등록(f"물건_{5}", 1000, 1, eletronics),
        ]

        def eyes(id):
            try:
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
                        cnt = Product.objects.filter(type_id=id).count()
                        print(cnt)
                        self.상품_등록(f"물건_{int(time.time())}", 1000, 1, cloth),
                return True
            except Exception as e:
                print(f"### {e}")
                return False

        args_list = []
        for product in products:
            args_list.append((product.type.id))

        time.sleep(2)

        results = []

        with ThreadPoolExecutor(max_workers=product_cnt) as executor:
            futures = [executor.submit(eyes, arg) for arg in args_list]
            for future in as_completed(futures):
                result = future.result()
                if future.done():
                    results.append(result)
                else:
                    future.cancelled()

        for type in ProductType.objects.all():
            print(type.name)
