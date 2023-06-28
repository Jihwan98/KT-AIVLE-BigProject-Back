from rest_framework import status, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .models import *
from accounts.models import *
from .serializers import *
from .ai_inference import class_model_inference
from .gpt import chatGPT_disease, chatGPT_answer
from rest_framework.generics import get_object_or_404
from rest_framework.filters import SearchFilter
import threading

# Create your views here.

# posts/api/Picture     
class PictureViewSet(ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def create(self, request):
        try:
            # 등록하려는 pet_id 가 user의 pet인지 확인
            pet_id = request.data.get('pet_id')
            if pet_id and request.user != Pet.objects.filter(id=pet_id).first().ownerid:
                return Response({"message": "해당 유저에 등록되지 않은 반려동물입니다."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            photo_io = serializer.validated_data['photo'].file
            disease, conf = class_model_inference(photo_io)
            serializer.validated_data['model_result'] = disease
            serializer.validated_data['model_conf'] = conf

            # serializer.validated_data['gpt_explain'] = chatGPT_disease(conf, disease) # GPT 질병 설명

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response(f"error : {e}", status=status.HTTP_400_BAD_REQUEST)
# 유저 Picture 이력 조회
# posts/api/picture-list-my/
class PictureList(generics.ListCreateAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(userid=self.request.user)
        return queryset

# question pagination 추가
class QuestionPagination(PageNumberPagination):
    page_size = 10

# posts/api/Question
class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = QuestionPagination
    
    # 검색 기능
    # posts/api/question/?search={검색어}
    filter_backends = [SearchFilter] # SearchFilter 기반으로 검색
    search_fields = ('title', 'contents', ) # 어떤 컬럼을 기반으로 검색할 건지 튜플 형식으로 작성

    def create(self, request):
        try:
            # 등록하려는 picture 가 user의 picture인지 확인
            pictureid = request.data.get('pictureid')
            pic = Picture.objects.filter(id=pictureid).first()
            if request.user != pic.userid:
                return Response({"message": "해당 유저에 등록되지 않은 사진입니다."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            gpt_args = {
                "disease" : pic.model_result,
                "confidence" : float(pic.model_conf),
                "title" : serializer.data['title'],
                "contents" : serializer.data['contents']
            }
            # GPT 쓰레드를 시작
            t = threading.Thread(
                target=self.gpt_thread, 
                args=(gpt_args, serializer.data['id'])
            )
            # t.daemon = True
            t.start()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response(f"error : {e}", status=status.HTTP_400_BAD_REQUEST)
    def gpt_thread(self, gpt_args, questionid):
        """_summary_

        Args:
            gpt_args (dict) :
                disease (str): 모델이 사진을 보고 예측한 병명
                confidence (float): 모델이 해당 병명을 예측한 확률
                title (str): 질문 제목
                contents (str): 질문 내용
            questionid (int) : questionid(pk)
        Returns:
            _type_: _description_
        """
        print("------------GPT THREAD START------------")
        # chatGPT 답변
        gpt_answer = chatGPT_answer(
            gpt_args['disease'], 
            gpt_args['confidence'], 
            gpt_args['title'], 
            gpt_args['contents']
        )
        print("gpt_answer :", gpt_answer)
        # answer 등록
        ans = Answer(userid=User.objects.get(id=26), # id 값은 User에서 GPT 계정으로 해야함
                     questionid=Question.objects.get(id=questionid), 
                     contents=gpt_answer)
        ans.save()
        
        print("------------GPT THREAD FINISH-----------")
        

# 유저 Question 이력 조회
# posts/api/question-list-my/
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(userid=self.request.user)
        return queryset

# /posts/question/<int:question:id>/answer : Question 별 Answer 조회 및 생성
# /posts/question/<int:question:id>/answer/<int:id> : Answer 수정 및 삭제
class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(questionid=self.kwargs["questionid"]) # url로 받은 인자는 self.kwargs['키워드'] 를 통해 접근 가능
        return queryset
    
    def perform_create(self, serializer):
        question = Question.objects.get(id=self.kwargs["questionid"])
        serializer.save(userid=self.request.user, questionid=question)
        return super().perform_create(serializer)
    

