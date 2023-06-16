from django.contrib import admin
from .models import *
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

# admin.site.unregister(Site)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    pass

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    pass

