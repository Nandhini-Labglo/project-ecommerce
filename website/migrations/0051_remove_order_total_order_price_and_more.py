# Generated by Django 4.1.2 on 2022-11-09 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0050_remove_payment_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_order_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_product_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_tax',
        ),
    ]