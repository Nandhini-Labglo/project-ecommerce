# Generated by Django 4.1.2 on 2022-10-26 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0023_alter_cart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='order_pl',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
