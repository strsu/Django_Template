from django.test import TransactionTestCase

from api.v1.user.models import User
from api.v1.model_view_set.models import Product, ProductOrder

from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# python manage.py test api/v1/model_view_set/tests/
# python manage.py test api/v1/model_view_set/tests --settings='config.settings.test_real_db'


class ProductTest(TransactionTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def tearDown(self):
        pass

    def 상품_등록(self, name, price, count):
        self.product = Product.objects.create(
            name=name, price=price, remaining_items=count
        )

    def 구매자_생성(self, count=1):
        self.user_list = []
        for i in range(count):
            self.user_list.append(User.objects.create(email=f"user_{i}"))

    def test_상품_동시_구매(self):

        num_user = 10
        remain = 7
        self.상품_등록("물건", 1000, remain)
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
                    self.product.id,
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

        print(Product.objects.get(id=self.product.id).__dict__)

        self.assertEqual(results.count(True), remain)
