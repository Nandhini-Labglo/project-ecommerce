# Generated by Django 4.1.2 on 2022-11-09 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0053_alter_order_total_order_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='paid',
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_status',
            field=models.IntegerField(choices=[(1, 'Success'), (0, 'Failed'), (2, 'Pending')], default=2),
        ),
    ]