from rest_framework import serializers
from .models import Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id']

class QuestionListSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True, read_only= True)
    answer_count = serializers.IntegerField(source='answer_set.count', read_only=True)

    class Meta:
        model = Question
        fields =  '__all__'
