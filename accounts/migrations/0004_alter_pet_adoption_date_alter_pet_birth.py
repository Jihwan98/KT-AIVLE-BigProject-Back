# Generated by Django 4.1 on 2023-06-14 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_adoptiondate_pet_adoption_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='adoption_date',
            field=models.DateField(blank=True, db_column='adoptionDate', null=True),
        ),
        migrations.AlterField(
            model_name='pet',
            name='birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]