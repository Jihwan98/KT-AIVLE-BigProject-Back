from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import *
from .serializers import *
from .ai_inference import ai_model_inference
# from rest_framework.generics import ListAPIView
# Create your views here.

# posts/api/Picture     
class PictureViewSet(ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(userid=self.request.user)
        return queryset
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        photo_io = serializer.validated_data['photo'].file
        serializer.validated_data['model_result'] = ai_model_inference(photo_io)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# posts/api/Question     
class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(userid=self.request.user)
        return queryset