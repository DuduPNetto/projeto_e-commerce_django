# Generated by Django 4.2.2 on 2023-06-26 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_product_promotional_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='promotional_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
