from django.contrib import admin
from .models import *
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.utils.safestring import mark_safe

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_vet', 'avatar']
    list_display_links= ['email', 'avatar']
    
    def avatar(self, user):
        return mark_safe(f"<img src={user.avatar} style='width: 100px;' />")
    
    def avatar_url(self, user):
        return user.avatar

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    pass

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    pass

