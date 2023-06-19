from django.contrib import admin
from .models import *
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.utils.safestring import mark_safe

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_vet', 'avatar','avatar_url']
    list_display_links= ['email', 'avatar']
    
    def avatar(self, user):
        return mark_safe(f"<img src={user.avatar} style='width: 100px;' />")
    
    def avatar_url(self, user):
        return user.avatar

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['hos_name', 'address', 'introduction', 'hos_profile_img_url']
    list_display_links= ['hos_name', 'address', 'introduction', 'hos_profile_img_url']
    
    def hos_profile_img_url(self, hospital):
        return mark_safe(f"<img src={hospital.hos_profile_img.url} style='width: 100px;' />")

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'ownerid', 'birth', 'gender']
    list_display_links= ['name', 'species', 'ownerid', 'birth', 'gender']

