# Generated by Django 4.1.2 on 2022-11-01 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0034_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_order_price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='total_product_price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='total_tax',
            field=models.FloatField(null=True),
        ),
    ]