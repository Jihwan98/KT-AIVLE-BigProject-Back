from rest_framework import serializers
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
        read_only_fields = ['id', 'userid', 'created_at', 'model_result']
    # 생성시에는 user에 접근하여 userid에 값을 넣도록
    def create(self, validated_data):
        validated_data["userid"] = self.context['request'].user
        pic = Picture.objects.create(**validated_data)
        pic.save()
        return pic
    
class QuestionSerializer(ModelSerializer):
    answer_set = AnswerSerializer(many=True, read_only=True)
    answer_count = serializers.IntegerField(source='answer_set.count', read_only=True)
    user_name = serializers.SerializerMethodField('get_user_name')
    class Meta:
        model = Question
        fields = '__all__'

    # 생성시에는 user에 접근하여 userid에 값을 넣도록
    def create(self, validated_data):
        validated_data["userid"] = self.context['request'].user
        question = Question.objects.create(**validated_data)
        question.save()
        return question

    def get_user_name(self, obj):
        user = obj.userid
        return user.first_name