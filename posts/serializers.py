from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *
from accounts.models import Hospital
from django.contrib.auth import get_user_model
from accounts.models import User

# Posts 앱에서 user에 접근할 때 사용
# class UsersimpleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id']

class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
        read_only_fields = ['id', 'userid', 'created_at', 'model_result'] 
    
    
    def create(self, validated_data):
        validated_data["userid"] = self.context['request'].user # 생성시에는 user에 접근하여 userid에 값을 넣도록
        pic = Picture.objects.create(**validated_data)
        pic.save()
        return pic
    
class QuestionSerializer(ModelSerializer):
    answer_count = serializers.IntegerField(source='answer_set.count', read_only=True)
    user_name = serializers.SerializerMethodField('get_user_name')
    
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['id', 'userid', 'created_at', 'model_result', 'pictureid', 'updated_at']

    # 생성시에는 user에 접근하여 userid에 값을 넣도록
    def create(self, validated_data):
        validated_data["userid"] = self.context['request'].user
        question = Question.objects.create(**validated_data)
        question.save()
        return question

    def get_user_name(self, obj):
        user = obj.userid
        return user.first_name
    
class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"

class AnswerSerializer(ModelSerializer):
    hospital = HospitalSerializer(source='userid.hospital', read_only=True)
    
    class Meta:
        model = Answer
        fields = ['id', 'userid', 'title', 'contents', 'questionid', 'hospital']
        read_only_fields = ['id', 'userid', 'questionid', 'hospital']