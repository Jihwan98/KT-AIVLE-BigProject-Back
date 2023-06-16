# Generated by Django 4.2.2 on 2023-06-16 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_user_email_alter_user_is_vet"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hospital",
            name="user_id",
            field=models.OneToOneField(
                db_column="user_id",
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]