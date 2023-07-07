from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from django.conf import settings
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from .models import *
from .permissions import *
import random
from django.db.models import Count
import numpy as np

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
            # chatgpt 제외, 답변 0개 제외, 답변 개수 세기
            # hos = Hospital.objects.exclude(hos_name="ChatGPT").filter(user_id__answer__isnull=False).annotate(answer_count=Count('user_id__answer'))
            # chatgpt 제외, 답변 개수 세기
            hos = Hospital.objects.exclude(hos_name="ChatGPT").annotate(answer_count=Count('user_id__answer')) 
            if hos: # 병원 정보가 존재하면
                # ans_count = np.array(list(map(lambda x: x['answer_count'], hos.values('answer_count'))))
                ans_count = np.array(list(map(lambda x: x['answer_count'] + 1, hos.values('answer_count')))) # 기본 1개를 줘서 광고에 노출 될 수 있도록
                ans_prob = ans_count / sum(ans_count) # 답변 개수에 따른 확률
                idx = np.random.choice(len(hos), p=ans_prob) # 답변 개수에 따른 광고 빈도 
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