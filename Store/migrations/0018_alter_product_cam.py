# Generated by Django 3.2 on 2021-09-28 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0017_product_cam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Cam',
            field=models.IntegerField(blank=True, default=15, null=True),
        ),
    ]
