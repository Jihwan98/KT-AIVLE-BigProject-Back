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

# accounts/api/Picture     
class PictureViewSet(ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(user_id=self.request.user)
        return queryset

# accounts/api/Question     
class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(user_id=self.request.user)
        return queryset
