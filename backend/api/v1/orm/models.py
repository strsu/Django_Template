from django.db import models


class Price(models.Model):
    date = models.DateField()
    time = models.IntegerField()

    values = models.FloatField()

    class Meta:
        verbose_name = "price"


class PowerGeneration(models.Model):

    power_decimal = models.DecimalField(
        "현재출력",
        max_digits=20,  # 전체 자리수를 20으로 설정, 20을 넘어가면 숫자가 잘린다!!!
        decimal_places=6,
    )
    power_float = models.FloatField("현재출력")

    class Meta:
        verbose_name = "발전량"
