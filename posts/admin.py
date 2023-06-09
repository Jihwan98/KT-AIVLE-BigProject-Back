from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    pass