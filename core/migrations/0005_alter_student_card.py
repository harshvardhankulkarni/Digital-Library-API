# Generated by Django 5.0 on 2023-12-30 04:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_card_created_on_alter_student_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='card',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.card'),
        ),
    ]
