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

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['contents']
    
class ChatGptQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['contents', 'title', 'model_result']

class ChatGptAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['contents']