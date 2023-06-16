from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Question, Answer
from settings_params import *
from .serializers import QuestionListSerializer, ChatGptQuestionSerializer, ChatGptAnswerSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.conf import settings
import openai
openai.api_key = settings.OPENAI_API_KEY
# Create your views here.

class QuestionListView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer
    
    def get_queryset(self):
        return Question.objects.filter(is_question=True)


class ChatGptAnswerAPIView(APIView):
    def generate_prompt(q1, q2, q3):
        return (f"사용자가 해당 질문에 대해서 물어보면, 질문의 제목과 해당 질병에 대한 정보 \
            를 바탕으로, 질문의 내용에 대해서, \
            너가 답변을 해줘. 해당 질병은 어떠한 상태로 보이며 \
            해당 질병에 대해 어떻게 보호자가 치료를 하는 것이 좋을지 \
            보호자가 유의해야할 부분이 무엇인지 알려줘.  \n\n \
            질문의 제목: {q1} \n \
            질병명: {q2} \n \
            질문의 내용: {q3}")
    
    
    def post(self, request):
        serializer = ChatGptQuestionSerializer(data=request.data)
        # validated_data: 유효성 검사를 통과한 필드에 접근
        if serializer.is_valid():
            question_title = serializer.validated_data['title']
            question_result = serializer.validated_data['model_result']
            question_content = serializer.validated_data['contents']
            response = openai.Completion.create(
                model = "",
                prompt = generate_prompt(Question.title, Question.model_result, Question.contents),
                max_tokens = 100,
                temperature = 0.5,
            )
            response = response.choices[0].text.strip()
            # create해라.
            answer = Answer.objects.create(contents=response)
            answer.save()
            return Response({'response': response})
            
            
            
    
    
    
    
    

