from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Picture, Question, History, Answer
from .serializers import PictureSerializer, QuestionSerializer, HistorySerializer, AnswerSerializer
# Create your views here.

# viewset: crud api 생성
class PictureViewSet(ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer    

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class HistoryViewSet(ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer