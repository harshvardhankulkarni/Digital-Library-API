# Generated by Django 5.0 on 2023-12-30 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_card_valid_up_to_alter_student_created_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='created_on',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='created_on',
            field=models.DateField(auto_now_add=True),
        ),
    ]