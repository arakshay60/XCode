# Generated by Django 4.2.9 on 2024-01-24 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OJ', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='description',
            field=models.TextField(blank=True, max_length=10000),
        ),
    ]
