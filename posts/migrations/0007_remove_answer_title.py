# Generated by Django 4.1 on 2023-06-23 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_question_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='title',
        ),
    ]
