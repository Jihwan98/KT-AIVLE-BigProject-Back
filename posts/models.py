from django.db import models
from django.utils import timezone
# Create your models here.

class Picture(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='UserID', blank=False)  # Field name made lowercase.
    photo = models.ImageField(upload_to="picture/post/", null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    model_result= models.CharField(max_length=255, blank=True, null=True) # 모델링 결과
    pet_id= models.ForeignKey('accounts.Pet', on_delete=models.CASCADE, db_column='PetID', blank=True, null=True)
    
    class Meta:
        db_table = 'picture'
    def __str__(self) -> str:
        return f"userid : {self.userid}, pet_id : {self.pet_id}"
        
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='UserID', blank=False)  # Field name made lowercase.
    pictureid = models.ForeignKey('Picture', on_delete=models.CASCADE, db_column='PictureID', blank=False, null=False)

    title = models.CharField(db_column='Title', max_length=32, blank=True, null=True)  # Field name made lowercase.
    contents = models.CharField(db_column='Contents', max_length=255, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'question'
    def __str__(self) -> str:
        return self.title

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='UserID')  # Field name made lowercase.
    questionid = models.ForeignKey('Question', on_delete=models.CASCADE, db_column='Questionid')  # Field name made lowercase.
    title = models.CharField(db_column='TItle', max_length=32)  # Field name made lowercase.
    contents = models.CharField(db_column='Contents', max_length=255)  # Field name made lowercase.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'answer'


