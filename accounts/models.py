from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, null=False, blank=False)
    
    # 반려인(False), 수의사(True)
    is_vet = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    # @property
    # def name(self):
    #     return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'user'

class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    hos_name = models.CharField(max_length=255, blank=True, null=True) # 병원이름
    address = models.CharField(max_length=255, blank=True, null=True)
    officenumber = models.CharField(db_column='officeNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    introduction = models.CharField(max_length=255, blank=True, null=True) # 자기소개
    
    class Meta:
        db_table = 'hospital'
        
class Pet(models.Model):
    
    class GenderChoices(models.TextChoices):
        MALE = "M", "수컷"
        FEMALE = "F", "암컷"    
    
    id = models.AutoField(primary_key=True)
    ownerid = models.ForeignKey("User", on_delete=models.CASCADE, db_column='ownerID')  # Field name made lowercase.
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, choices=GenderChoices.choices)
    is_neu = models.BooleanField(default=False) # 중성화여부 (True: 중성화)
    adoption_date = models.DateField(db_column='adoptionDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'pet'