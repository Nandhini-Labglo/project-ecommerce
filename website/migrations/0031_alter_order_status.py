# Generated by Django 4.1.2 on 2022-11-01 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0030_alter_brand_brand_name_alter_brand_created_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Success'), (2, 'Pending'), (0, 'Failed')], default='Pending', max_length=120),
        ),
    ]
