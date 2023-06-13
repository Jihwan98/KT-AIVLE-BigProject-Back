from rest_framework import serializers
from .models import Picture, Question, History, Answer

class  PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = "__all__"
        
class  QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        
class  HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"
        
class  AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"