from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Question, Answer
from .serializers import ListQuestionSerializer, QuestionSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
# Create your views here.

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def perform_create(self, serializer):
        serializer.save(userid=self.request.user, is_question = True)
        
    # 수정시, 사진이 날아가는 것 같은데 반드시 테스트 해볼 것! (테스트 후 주석 삭제)
    

class ListQuestionView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = ListQuestionSerializer
    
    def get_queryset(self):
        return Question.objects.filter(is_question=True)