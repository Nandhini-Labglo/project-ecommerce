# Generated by Django 4.1.2 on 2022-10-26 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_alter_cart_is_active_alter_cart_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
