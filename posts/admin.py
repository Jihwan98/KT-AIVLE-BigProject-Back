from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id',  'title', 'pictureid']
    list_display_links= ['id', 'title', 'pictureid']
    
    # def photo_tag(self, question):
    #     return mark_safe(f"<img src={question.photo.url} style='width: 100px;' />")
    
    # def photo_url(self, question):
    #     return question.photo.url
    

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['userid']
    list_display_links= ['userid']
    
@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass
    # list_display = ['preview_photo', 'model_result','created_at']
    # list_display_links= ['preview_photo', 'model_result', 'created_at']

    # def preview_photo(self, picture):
    #     return mark_safe(f"<img src={picture.photo.url} style='width: 100px;' />")
