from rest_framework import serializers
from .models import Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id']

class ListQuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True, read_only= True)
    answer_count = serializers.IntegerField(source='answer_set.count', read_only=True)

    class Meta:
        model = Question
        fields =  '__all__'
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields =  ['photo', 'title', 'contents', 'pet_id', 'userid']
        read_only_fields = ['userid']