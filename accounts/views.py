from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import *
from django.conf import settings
from django.shortcuts import redirect
import requests
from .models import User
from allauth.socialaccount.providers.naver import views as naver_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from json import JSONDecodeError
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import HospitalSerializer, PetSerializer
from django.core import serializers
from rest_framework import viewsets

main_domain = settings.MAIN_DOMAIN

# DB에 email 정보가 존재하는지 여부 판단
class EmailCheckAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists(): # 이미 DB에 해당 email이 존재
            return JsonResponse({"success": False, "message" : "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else: # 생성가능
            return JsonResponse({"success": True, "message" : "Available emails"}, status=status.HTTP_200_OK)

# DRF의 APIView를 상속받아 View를 구성
class NaverLoginAPIView(APIView):
    # 로그인을 위한 창은 누구든 접속이 가능해야 하기 때문에 permission을 AllowAny로 설정
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        client_id = settings.NAVER_CLIENT_ID
        response_type = "code"
        # Naver에서 설정했던 callback url을 입력해주어야 한다.
        # 아래의 전체 값은 http://127.0.0.1:8000/user/naver/callback 이 된다.
        uri = main_domain + "/user/naver/callback"
        state = settings.STATE
        # Naver Document 에서 확인했던 요청 url
        url = "https://nid.naver.com/oauth2.0/authorize"
        
        # Document에 나와있는 요소들을 담아서 요청한다.
        return redirect(
            f'{url}?response_type={response_type}&client_id={client_id}&redirect_uri={uri}&state={state}'
        )


class NaverCallbackAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        try:
            # Naver Login Parameters
            grant_type = 'authorization_code'
            client_id = settings.NAVER_CLIENT_ID
            client_secret = settings.NAVER_CLIENT_SECRET
            code = request.GET.get('code')
            state = request.GET.get('state')

            parameters = f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"

            # token request
            token_request = requests.get(
                f"https://nid.naver.com/oauth2.0/token?{parameters}"
            )

            token_response_json = token_request.json()
            error = token_response_json.get("error", None)

            if error is not None:
                raise JSONDecodeError(error)

            access_token = token_response_json.get("access_token")

            # User info get request
            user_info_request = requests.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            # User 정보를 가지고 오는 요청이 잘못된 경우
            if user_info_request.status_code != 200:
                return JsonResponse({"error": "failed to get email."}, status=status.HTTP_400_BAD_REQUEST)

            user_info = user_info_request.json().get("response")
            email = user_info["email"]

            # User 의 email 을 받아오지 못한 경우
            if email is None:
                return JsonResponse({
                    "error": "Can't Get Email Information from Naver"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(email=email)
                data = {'access_token': access_token, 'code': code}
                # accept 에는 token 값이 json 형태로 들어온다({"key"}:"token value")
                # 여기서 오는 key 값은 authtoken_token에 저장된다.
                accept = requests.post(
                    f"{main_domain}/user/naver/login/success", data=data
                )
                # 만약 token 요청이 제대로 이루어지지 않으면 오류처리
                if accept.status_code != 200:
                    return JsonResponse({"error": "Failed to Signin."}, status=accept.status_code)
                return Response(accept.json(), status=status.HTTP_200_OK)

            except User.DoesNotExist:
                data = {'access_token': access_token, 'code': code}
                accept = requests.post(
                    f"{main_domain}/user/naver/login/success", data=data
                )
                # token 발급
                return Response(accept.json(), status=status.HTTP_200_OK)
                
        except:
            return JsonResponse({
                "error": "error",
            }, status=status.HTTP_404_NOT_FOUND)
            
   
class NaverToDjangoLoginView(SocialLoginView):
    adapter_class = naver_views.NaverOAuth2Adapter
    client_class = OAuth2Client
    
# accounts/api/hospital     
class HospitalViewSet(ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer    

# accounts/api/pet 
class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(ownerid=self.request.user)
        return queryset