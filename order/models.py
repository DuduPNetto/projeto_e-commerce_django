from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(default="C", max_length=1, choices=(
        ('A', 'Aprovado'), ('C', 'Criado'), ('R', 'Reprovado'),
        ('P', 'Pendente'), ('E', 'Enviado'), ('F', 'Finalizado')
    ))

    def __str__(self) -> str:
        return f'Order N. {self.pk}'


class OrderItem(models.Model):
    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=100)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

    def __str__(self) -> str:
        return f'{self.order} Item'
