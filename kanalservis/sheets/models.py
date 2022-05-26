from django.db import models

from .utils.orders import from_usd_to_rub


class Order(models.Model):
    order_number = models.IntegerField('Номер заказа')
    usd_price = models.IntegerField('Стоимость в $')
    rub_price = models.FloatField('Стоимость в ₽', blank=True, null=True)
    delivery_date = models.DateField()

    def __str__(self):
        return str(self.order_number)

    def save(self, *args, **kwargs):
        print(from_usd_to_rub(self.usd_price))
        self.rub_price = from_usd_to_rub(self.usd_price)
        return super().save(*args, **kwargs)
