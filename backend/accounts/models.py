from django.conf import settings
from django.contrib.auth.models import AbstractUser
# from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    hospitalID = models.TextField(blank=True)
    
    # 휴대전화 번호
    # phone_number = models.CharField(
    #     max_length=13,
    #     blank=True,
    #     validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    # )

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
