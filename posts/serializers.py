from rest_framework.serializers import ModelSerializer
from .models import *

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id']

class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
    # 생성시에는 user에 접근하여 userid에 값을 넣도록
    def create(self, validated_data):
        validated_data["userid"] = self.context['request'].user
        pic = Picture.objects.create(**validated_data)
        pic.save()
        return pic
    
class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
    # 생성시에는 user에 접근하여 userid에 값을 넣도록
    def create(self, validated_data):
        validated_data["userid"] = self.context['request'].user
        question = Question.objects.create(**validated_data)
        question.save()
        return question