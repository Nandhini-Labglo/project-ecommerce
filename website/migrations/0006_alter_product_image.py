# Generated by Django 4.1.2 on 2022-10-20 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='images/products'),
        ),
    ]
