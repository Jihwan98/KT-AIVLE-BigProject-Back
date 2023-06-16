from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Question, Answer
from .serializers import ListQuestionSerializer, QuestionSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
# Create your views here.

class ListQuestionView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = ListQuestionSerializer
    
    def get_queryset(self):
        return Question.objects.filter(is_question=True)

class CreateQuestionView(CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def perform_create(self, serializer):
        serializer.save(userid=self.request.user, is_question = True)