# Generated by Django 4.1.2 on 2022-11-08 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0040_remove_payment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paid',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='transaction_id',
            field=models.IntegerField(),
        ),
    ]
