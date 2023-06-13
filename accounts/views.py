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
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from json import JSONDecodeError
from settings_params import *

main_domain = settings.MAIN_DOMAIN

# DRF의 APIView를 상속받아 View를 구성
class NaverLoginAPIView(APIView):
    # 로그인을 위한 창은 누구든 접속이 가능해야 하기 때문에 permission을 AllowAny로 설정
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        client_id = settings.NAVER_CLIENT_ID
        response_type = "code"
        # Naver에서 설정했던 callback url을 입력해주어야 한다.
        # 아래의 전체 값은 http://127.0.0.1:8000/user/naver/callback 이 된다.
        uri = main_domain + "/accounts/naver/callback"
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
                    f"{main_domain}/accounts/naver/login/success", data=data
                )
                # 만약 token 요청이 제대로 이루어지지 않으면 오류처리
                if accept.status_code != 200:
                    return JsonResponse({"error": "Failed to Signin."}, status=accept.status_code)
                return Response(accept.json(), status=status.HTTP_200_OK)

            except User.DoesNotExist:
                data = {'access_token': access_token, 'code': code}
                accept = requests.post(
                    f"{main_domain}/accounts/naver/login/success", data=data
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

# 카카오 로그인
class KakaoLoginAPIView(APIView):
    # 로그인
    permission_classes = (AllowAny, )
    
    def get(self, request, *args, **kwargs):
        # settings_param.py에 등록해둔 rest_api_key와 redirect_uri
        rest_api_key = settings.KAKAO_REST_API_KEY
        #rest_api_key = getattr(SOCIAL_LOGIN, 'KAKAO_REST_API_KEY')
        url = "https://kauth.kakao.com/oauth/authorize"
        #redirect_uri = getattr(KAKAO_REDIRECT_URI)
        redirect_uri = settings.KAKAO_REDIRECT_URI
        return redirect(
            f"{url}?client_id={rest_api_key}&redirect_uri={redirect_uri}&response_type=code")
        
# 카카오 리디렉션 
class KakaoCallbackAPIView(APIView):
    permission_classes = (AllowAny, )
    
    def get(self, request, *args, **kwargs):
        try:
            #rest_api_key = getattr(SOCIAL_LOGIN, 'KAKAO_REST_API_KEY')
            rest_api_key = settings.KAKAO_REST_API_KEY
            #redirect_uri = getattr(SOCIAL_LOGIN, 'KAKAO_REDIRECT_URI')
            redirect_uri = setting.KAKAO_REDIRECT_URI
            # 인가코드 가져오기
            code = request.GET.get('code')
            """
            Access Token Request
            """
            
            # token 받아오기
            data = {
                'grant_type': 'authorization_code',
                'client_id': rest_api_key,
                'redirect_uri': redirect_uri,
                'code': code
            }
            
            token_response = requests.post('https://kauth.kakao.com/oauth/token', data=data)
            token_response_json = token_response.json()
            error = token_response_json.get('error', None)
            
            if error is not None:
                raise JSONDecodeError(error)
            
            # 인가가능한 토큰 받아와서, 해당 유저 info_response받기
            access_token = token_response_json.get('access_token')
            """
            Email Request
            """
            headers = {'Authorization': f'Bearer {access_token}'}
            user_info_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers=headers    
            )
            # 만약 유저 정보를 가져올 수 없다면 에러 발생
            if user_info_request.status_code != 200:
                return JsonResponse({'error': 'failed to get user info'}, status=status.HTTP_400_BAD_REQUEST)
            
            user_info_json = user_info_request.json()
            kakao_account = user_info_json.get('kakao_account')
            
            print(kakao_account)
            # kakao account에서 이메일 가져오기.
            email = kakao_account.get('email')
            
            """
            Signup or Signin Request
            """
            
            try:
                user = User.objects.get(email=email)
                data = {'access_token': access_token, 'code': code}
                # accept 에는 token 값이 json 형태로 들어온다({"key"}:"token value")
                # 여기서 오는 key 값은 authtoken_token에 저장된다.
                accept = requests.post(
                    f"{main_domain}/accounts/kakao/login/success", data=data
                )
                # 만약 token 요청이 제대로 이루어지지 않으면 오류처리
                if accept.status_code != 200:
                    return JsonResponse({"error": "Failed to Signin."}, status=accept.status_code)
                return Response(accept.json(), status=status.HTTP_200_OK)

            except User.DoesNotExist:
                # 기존에 가입된 유저가 없으면 새로 가입
                data = {'access_token': access_token, 'code': code}
                accept = requests.post(
                    f"{main_domain}/accounts/kakao/login/success", data=data
                )
                # token 발급
                return Response(accept.json(), status=status.HTTP_200_OK)
                
        except:
            return JsonResponse({
                "error": "error",
            }, status=status.HTTP_404_NOT_FOUND)
            
class KakaoToDjangoLoginView(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.KAKAO_REDIRECT_URI
            
            
    