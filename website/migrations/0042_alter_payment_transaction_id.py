# Generated by Django 4.1.2 on 2022-11-08 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0041_payment_email_alter_payment_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='transaction_id',
            field=models.TextField(),
        ),
    ]