# Generated by Django 3.2 on 2021-09-14 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0007_alter_order_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=200),
        ),
    ]
