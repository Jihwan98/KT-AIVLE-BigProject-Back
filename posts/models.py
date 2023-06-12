from django.db import models

# Create your models here.

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='UserID')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=32)  # Field name made lowercase.
    contents = models.CharField(db_column='Contents', max_length=255)  # Field name made lowercase.
    pictureid = models.OneToOneField('Picture', on_delete=models.CASCADE, db_column='PictureID')  # Field name made lowercase.
    date = models.DateTimeField()

    class Meta:
        db_table = 'question'

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='UserID')  # Field name made lowercase.
    title = models.CharField(db_column='TItle', max_length=32)  # Field name made lowercase.
    contents = models.CharField(db_column='Contents', max_length=255)  # Field name made lowercase.
    questiontid = models.ForeignKey('Question', on_delete=models.CASCADE, db_column='QuestiontID')  # Field name made lowercase.
    date = models.DateTimeField()

    class Meta:
        db_table = 'answer'

class Picture(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=255)

    class Meta:
        db_table = 'picture'

class History(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='UserID')  # Field name made lowercase.
    pictureid = models.OneToOneField('Picture', on_delete=models.CASCADE, db_column='PictureID', unique=True)  # Field name made lowercase.
    date = models.DateTimeField()
    resultnum = models.IntegerField(db_column='resultNum')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255)  # Field name made lowercase.
    petid = models.OneToOneField('accounts.Pet', on_delete=models.CASCADE, db_column='PetID', unique=True)  # Field name made lowercase.

    class Meta:
        db_table = 'history'


