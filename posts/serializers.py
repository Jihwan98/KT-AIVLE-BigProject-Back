from rest_framework import serializers
from .models import Picture, Question

class  PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = "__all__"
        
class  QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"