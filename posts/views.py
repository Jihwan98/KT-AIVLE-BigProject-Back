from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Question, Answer
# from .serializers import QuestionSerializer
from rest_framework.generics import ListAPIView
# Create your views here.

# viewset: crud api 생성  


