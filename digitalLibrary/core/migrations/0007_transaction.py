# Generated by Django 5.0 on 2023-12-30 04:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_author_country_alter_book_genra_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField(auto_now_add=True)),
                ('book_due_date', models.DateField()),
                ('is_issued', models.BooleanField()),
                ('is_returned', models.BooleanField()),
                ('fine_amount', models.IntegerField()),
                ('status', models.BooleanField()),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.book')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.card')),
            ],
        ),
    ]
