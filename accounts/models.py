from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, null=False, blank=False)
    hospitalID = models.ForeignKey("Hospital", on_delete=models.CASCADE, blank=True, null=True, db_column="hospitalID")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'user'

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