# Generated by Django 4.2.9 on 2024-01-24 02:00

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('OJ', '0002_alter_problem_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='description',
            field=froala_editor.fields.FroalaField(default=''),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='input',
            field=froala_editor.fields.FroalaField(default=''),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='output',
            field=froala_editor.fields.FroalaField(default=''),
        ),
    ]
