from django.db import models
from main.models import Product, Bazar
from django.core.validators import MinValueValidator, MaxValueValidator

class Order(models.Model):
    """ Сведения о заказe"""

    Delivery_Availability = (
        ('S', 'Самовывоз'),
        ('K', 'Доставка курьером '),
        ('P', 'Доставка почтовой службой '),

    )
    Paymen_Availability = (
        ('N', 'Наличные при получении'),
        ('C', 'Картой'),
        ('E', 'Электронные деньги'),
        ('B', 'Банковский перевод'),
    )


    fio = models.CharField(max_length=50)
    email = models.EmailField()
    delivery = models.CharField(max_length=1, choices=Delivery_Availability, default='S')  # доставка
    bazar = models.ForeignKey(Bazar, related_name='bazar', on_delete=models.CASCADE,null=True)
    payment = models.CharField(max_length=1, choices=Paymen_Availability, default='C')  # способ оплаты
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    oplata = models.BooleanField(default=False) # оплачен или нет

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())   # общая стоимость


class OrderItem(models.Model):
    """ Готовые заказы """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tel = models.CharField(max_length=11, db_index=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity   # возврат стоимости товара

class Kupon(models.Model):
    """Скидка по купонам """
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code