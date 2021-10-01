# Generated by Django 3.2 on 2021-09-16 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0010_orderitem_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='order',
            name='complete',
            field=models.CharField(choices=[('In progress', 'In progress'), ('Completed', 'Completed'), ('Delayed', 'Delayed'), ('Pending', 'Pending')], max_length=15),
        ),
    ]
