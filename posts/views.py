from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
# from .models import Picture, Question, Answer
# from .serializers import PictureSerializer, QuestionSerializer
# Create your views here.

# viewset: crud api 생성
# class PictureViewSet(ModelViewSet):
#     queryset = Picture.objects.all()
#     serializer_class = PictureSerializer    

# class QuestionViewSet(ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

# class AnswerViewSet(ModelViewSet):
#     queryset = Answer.objects.all()
#     serializer_class = AnswerSerializer