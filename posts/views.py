from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Question, Answer
from .serializers import QuestionListSerializer
# from rest_framework.generics import ListAPIView
# Create your views here.

# class QuestionListView(ListAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionListSerializer
    
#     def get_queryset(self):
#         return Question.objects.filter(is_question=True)

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer
    
    def get_queryset(self):
        return Question.objects.filter(is_question=True)

