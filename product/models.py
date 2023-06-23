from django.db import models

from utils.resize_image import resize_image


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    name = models.CharField(max_length=100)
    short_description = models.TextField()
    long_description = models.TextField()
    image = models.ImageField(
        upload_to='image_products/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    product_type = models.CharField(
        default='V', max_length=1, choices=(('V', 'Variação'), ('S', 'Simples'))
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.image:
            resize_image(self.image, max_image_size)

    def __str__(self) -> str:
        return self.name


class Variation(models.Model):
    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.name or self.product.name
