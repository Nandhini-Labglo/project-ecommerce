# Generated by Django 4.1.2 on 2022-10-29 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0026_alter_cart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
