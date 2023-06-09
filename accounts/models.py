from django.conf import settings
from django.contrib.auth.models import AbstractUser
# from django.core.validators import RegexValidator
from django.db import models

class Hospital(models.Model):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=255)
    officenumber = models.CharField(db_column='officeNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'hospital'
        
class Pet(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    birth = models.DateTimeField()
    ownerid = models.ForeignKey("User", on_delete=models.CASCADE, db_column='ownerID')  # Field name made lowercase.
    gender = models.IntegerField(blank=True, null=True)
    neutralization = models.IntegerField(blank=True, null=True)
    adoptiondate = models.DateTimeField(db_column='adoptionDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'pet'

class User(AbstractUser):
    hospitalID = models.ForeignKey("Hospital", on_delete=models.CASCADE, blank=True, null=True, db_column="hospitalID")
    
    # 휴대전화 번호
    # phone_number = models.CharField(
    #     max_length=13,
    #     blank=True,
    #     validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    # )

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
