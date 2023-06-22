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
from .ai_inference import ai_model_inference
from rest_framework.generics import get_object_or_404
# from rest_framework.generics import ListAPIView
# Create your views here.

# posts/api/Picture     
class PictureViewSet(ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(userid=self.request.user)
        return queryset
    
    def create(self, request):
        # 등록하려는 pet_id 가 user의 pet인지 확인
        pet_id = request.data.get('pet_id')
        if request.user != Pet.objects.filter(id=pet_id).first().ownerid:
            return Response({"message": "해당 유저에 등록되지 않은 반려동물입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        photo_io = serializer.validated_data['photo'].file
        serializer.validated_data['model_result'] = ai_model_inference(photo_io)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
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

    def create(self, request):
        # 등록하려는 picture 가 user의 picture인지 확인
        pictureid = request.data.get('pictureid')
        if request.user != Picture.objects.filter(id=pictureid).first().userid:
            return Response({"message": "해당 유저에 등록되지 않은 사진입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
    
# class QuestionSearchViewset(ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         keyword = self.request.query_params.get('keyword', None)
#         if keyword=='title':
#             queryset = queryset.filter(title__icontains=keyword)
#         elif keyword == 'contents':
#             queryset = queryset.filter(content__icontains=keyword)
#         return queryset
    
#     def create(self, request):
#         # 등록하려는 picture 가 user의 picture인지 확인
#         pictureid = request.data.get('pictureid')
#         if request.user != Picture.objects.filter(id=pictureid).first().userid:
#             return Response({"message": "해당 유저에 등록되지 않은 사진입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
    
    
