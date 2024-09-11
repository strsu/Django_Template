from django.test import Client, TestCase
from django.db.models import Sum

from api.v1.orm.models import PowerGeneration

from decimal import Decimal
import random

# python manage.py test api.v1.orm.tests.test_power_generation
# python manage.py test api/v1/orm/tests --settings='config.settings.test_real_db'


class DecimalTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        total_cnt = 10000
        obj_list = []

        for _ in range(total_cnt):
            v = round(random.randint(1000000, 1000000000) / 1000, 6)
            obj_list.append(PowerGeneration(power_decimal=v, power_float=v))

        PowerGeneration.objects.bulk_create(obj_list, batch_size=1000)

    def test_DB_합_결과(self):

        pg = PowerGeneration.objects.aggregate(
            decimal=Sum("power_decimal"), float=Sum("power_float")
        )

        v_float_sum = 0
        v_decimal_sum = Decimal(0)
        v_decimal_str_sum = Decimal("0")
        for value in PowerGeneration.objects.all():
            v_d = Decimal(value.power_float)
            v_ds = Decimal(str(value.power_float))
            v_float_sum += value.power_float
            v_decimal_sum += v_d
            v_decimal_str_sum += v_ds

        self.assertEqual(v_float_sum, pg.get("float"))
        self.assertEqual(v_decimal_str_sum, pg.get("decimal"))

        print(
            f"v_float_sum: {v_float_sum}, v_decimal_sum: {v_decimal_sum}, v_decimal_str_sum: {v_decimal_str_sum}"
        )

        print(pg)
