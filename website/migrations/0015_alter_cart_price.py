# Generated by Django 4.1.2 on 2022-10-25 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_alter_cart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
