# Generated by Django 4.1 on 2023-06-15 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_remove_question_pictureid_question_is_question_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='questiontid',
            new_name='questionid',
        ),
    ]
