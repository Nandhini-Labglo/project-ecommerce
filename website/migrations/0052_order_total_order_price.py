# Generated by Django 4.1.2 on 2022-11-09 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0051_remove_order_total_order_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_order_price',
            field=models.FloatField(null=True),
        ),
    ]