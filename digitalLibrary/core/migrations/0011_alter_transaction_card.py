# Generated by Django 5.0 on 2023-12-31 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_student_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.card'),
        ),
    ]
