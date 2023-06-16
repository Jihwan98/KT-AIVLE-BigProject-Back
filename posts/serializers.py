from rest_framework import serializers
from .models import Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id']

class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
    # 생성시에는 user에 접근하여 userid에 값을 넣도록
    def create(self, validated_data):
        validated_data["user_id"] = self.context['request'].user
        hos = Hospital.objects.create(**validated_data)
        hos.save()
        return hos
    
class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
    # 생성시에는 user에 접근하여 ownerid에 값을 넣도록
    def create(self, validated_data):
        validated_data["user_id"] = self.context['request'].user
        hos = Hospital.objects.create(**validated_data)
        hos.save()
        return hos