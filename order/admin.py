from django.contrib import admin

from order import models


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'product_id', 'variation',
                    'price', 'promotional_price', 'quantity')
    list_display_links = ('id', 'product', 'product_id')
    search_fields = ('id', 'product', 'product_id')
    ordering = ('-id',)
    list_filter = ('id',)
    list_editable = ('variation', 'price', 'promotional_price', 'quantity')


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 1


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user', 'status')
    ordering = ('-id',)
    list_filter = ('id',)
    list_editable = ('total', 'status')
    inlines = [OrderItemInline]
