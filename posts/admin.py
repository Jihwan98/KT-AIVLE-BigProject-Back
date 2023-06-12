from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo_tag', 'photo_url']
    list_display_links= ['id', 'photo_tag']
    
    def photo_tag(self, picture):
        return mark_safe(f"<img src={picture.photo.url} style='width: 100px;' />")
    
    def photo_url(self, picture):
        return picture.photo.url
        
        
    
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    pass