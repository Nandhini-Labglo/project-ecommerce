# Generated by Django 4.1.2 on 2022-10-25 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_order_pl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.FloatField(),
        ),
    ]
