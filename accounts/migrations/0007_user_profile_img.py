# Generated by Django 4.2.2 on 2023-06-16 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_hospital_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_img",
            field=models.ImageField(
                default="profile/default.png", upload_to="profile/"
            ),
        ),
    ]