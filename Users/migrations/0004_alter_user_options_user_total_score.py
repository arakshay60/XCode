# Generated by Django 4.2.9 on 2024-01-27 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_alter_submission_code_alter_submission_stderr_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-total_score']},
        ),
        migrations.AddField(
            model_name='user',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
    ]
