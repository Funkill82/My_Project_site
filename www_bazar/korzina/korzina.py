from decimal import Decimal
from django.conf import settings
from main.models import Product
from orders.models import Kupon

class Korzina(object):

    def __init__(self, request):
        """  Создаем корзину """
        self.session = request.session  # текущая сессия
        korzina = self.session.get(settings.KORZINA_SESSION_ID)

        if not korzina:
            korzina = self.session[settings.KORZINA_SESSION_ID] = {}  # сохраняю пустую корзину в сеансе
        self.korzina = korzina
        self.kupon_id = self.session.get('kupon_id')

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.korzina.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.korzina[str(product.id)]['product'] = product

        for item in self.korzina.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.korzina.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.korzina.values())


    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.korzina:
            self.korzina[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.korzina[product_id]['quantity'] = quantity
        else:
            self.korzina[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии korzina
        self.session[settings.KORZINA_SESSION_ID] = self.korzina
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.korzina:
            del self.korzina[product_id]
            self.save()

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.KORZINA_SESSION_ID]
        self.session.modified = True

    @property
    def kupon(self):
        if self.kupon_id:
            return Kupon.objects.get(id=self.kupon_id)
        return None

    def get_discount(self):
        if self.kupon:
            return (self.kupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()