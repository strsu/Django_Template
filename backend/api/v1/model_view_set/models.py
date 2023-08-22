from django.db import models


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

    demo_1 = models.CharField("demo", max_length=64, null=True, blank=True)
    demo_2 = models.CharField("demo", max_length=64, null=True, blank=True)
    demo_3 = models.CharField("demo", max_length=64, null=True, blank=True)
    demo_4 = models.CharField("demo", max_length=64, null=True, blank=True)
    demo_5 = models.CharField("demo", max_length=64, null=True, blank=True)
    demo_6 = models.CharField("demo", max_length=64, null=True, blank=True)

    class Meta:
        db_table = "product"
