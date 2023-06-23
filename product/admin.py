from django.contrib import admin

from product import models


@admin.register(models.Variation)
class Variation(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'price',
                    'promotional_price', 'stock')
    list_display_links = ('id', 'product', 'name')
    search_fields = ('id', 'product', 'name')
    ordering = ('-id',)
    list_filter = ('id',)
    list_editable = ('price', 'promotional_price', 'stock')


class VariationInline(admin.TabularInline):
    model = models.Variation
    extra = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'price',
                    'promotional_price', 'product_type')
    list_display_links = ('id', 'name', 'slug')
    search_fields = ('id', 'name', 'slug')
    ordering = ('-id',)
    list_filter = ('id',)
    list_editable = ('price', 'promotional_price', 'product_type')
    inlines = [VariationInline]
