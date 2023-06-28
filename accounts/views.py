from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from django.conf import settings
from django.shortcuts import redirect
import requests
from .models import User
from allauth.socialaccount.providers.naver import views as naver_views
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.views import UserDetailsView
from django.http import JsonResponse
from json import JSONDecodeError
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import HospitalSerializer, PetSerializer
from django.core import serializers
from rest_framework import viewsets
from allauth.socialaccount.models import SocialAccount
from rest_framework.generics import RetrieveUpdateAPIView
from .permissions import *
import random


main_domain = settings.MAIN_DOMAIN

class DeleteAccount(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user=self.request.user
        user.delete()

        return Response({"result":"user delete"})

# DB에 email 정보가 존재하는지 여부 판단
class EmailCheckAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            email = request.data.get('email')
            if User.objects.filter(email=email).exists(): # 이미 DB에 해당 email이 존재
                return JsonResponse({"success": False, "message" : "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            else: # 생성가능
                return JsonResponse({"success": True, "message" : "Available emails"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"error : {e}", status=status.HTTP_400_BAD_REQUEST)

# accounts/api/hospital/
class HospitalViewSet(ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated, IsVetAuthenticated, IsOwner]
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(user_id=self.request.user)
        return queryset

# accounts/api/hospital-ad/
class HospitalAdAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        try:
            hos = Hospital.objects.exclude(hos_name="ChatGPT") # chatgpt 제외
            if hos: # 병원 정보가 존재하면
                idx = random.randint(0, len(hos) - 1)
                data = HospitalSerializer(hos[idx]).data
                return Response({"hospital": data}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"message": "등록된 병원 정보 0개 입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"error : {e}", status=status.HTTP_400_BAD_REQUEST)

# accounts/api/pet/
class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(ownerid=self.request.user)
        return queryset