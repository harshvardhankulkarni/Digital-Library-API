# Generated by Django 5.0 on 2023-12-30 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='fine_amount',
            field=models.IntegerField(default=0),
        ),
    ]