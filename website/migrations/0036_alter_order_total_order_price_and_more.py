# Generated by Django 4.1.2 on 2022-11-01 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0035_order_total_order_price_order_total_product_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_order_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_product_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_tax',
            field=models.FloatField(),
        ),
    ]