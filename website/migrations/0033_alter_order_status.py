# Generated by Django 4.1.2 on 2022-11-01 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0032_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Success'), (0, 'Failed'), (2, 'Pending')], default='Pending'),
        ),
    ]
