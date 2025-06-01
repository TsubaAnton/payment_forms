from django.contrib import admin
from .models import Item, Discount, Tax, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency')
    search_fields = ('name', )


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percentage', 'stripe_id')
    search_fields = ('name', )


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_percentage', 'stripe_id', 'application')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_display')

    def total_display(self, obj):
        return f"{obj.calculate_total() / 100:.2f}"
    total_display.short_description = 'Total'


