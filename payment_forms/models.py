from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Item(models.Model):
    CURRENCY_CHOICES = [
        ('eur', 'EUR'),
        ('usd', 'USD'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd', verbose_name='Валюта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Discount(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    discount_percentage = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Процент скидки')
    stripe_id = models.CharField(max_length=255, verbose_name='ID скидки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Tax(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    tax_percentage = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Процент налога')
    stripe_id = models.CharField(max_length=255, verbose_name='ID налога')
    application = models.BooleanField(default=False, verbose_name='Применяется ли налог')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'


class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name='Товары')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, verbose_name='Скидка', **NULLABLE)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, verbose_name='Налог', **NULLABLE)

    def calculate_total(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total -= total * (self.discount.discount_percentage / 100)
        if self.tax and not self.tax.application:
            total += total * (self.tax.tax_percentage / 100)
        return int(total * 100)

    @property
    def display_total(self):
        total = self.calculate_total() / 100
        return f"{total:.2f}"

    def __str__(self):
        return f'{self.items} + {self.discount} + {self.tax}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

