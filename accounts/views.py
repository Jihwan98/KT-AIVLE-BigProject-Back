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
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
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
            

# google Login
class GoogleLoginAPIView(APIView):
    permission_classes = (AllowAny, )
    
    def get(self, request, *args, **kwargs):
        """
        code Request
        1. 매핑된 url로 들어가면, client_id, redirect할 uri 등과 같은 정보를
        url parameter로 함께 보내 리다이렉트한다. 그러면 구글 로그인 창이 뜨고, 알맞은
        아이디, 비밀번호로 진행하면 Callback URI로 Code값이 들어가게 된다.
        """
        client_id = settings.GOOGLE_CLIENT_ID
        response_type = "code"
        google_callback_uri = main_domain + "/accounts/google/callback"
        state = settings.STATE
        # google docs에서 확인했던 요청 url
        url = "https://accounts.google.com/o/oauth2/v2/auth"
        scope = "https://www.googleapis.com/auth/userinfo.email"
        return redirect(f"{url}?client_id={client_id}&response_type=code&redirect_uri={google_callback_uri}&scope={scope}")

class GoogleCallbackAPIView(APIView):
    """
    1. 전달받은 email과 동일한 Email이 있는지 찾아본다.
    2-1 만약 있다면?
    - socialaccount(소셜로그인한) 테이블에서 해당 이메일의 유저가 있는지 체크
    - 없으면 해당 계정은 일반계정(backend DB에 있는), 에러 메시지와 함께 400 리턴
    - 위 두개에 걸리지 않으면 로그인 진행, 해당 유저의 JWT발급, 그러나 중간에 예기치 못한 오류가 발생하면 에러메시지와 함께 오류 Status응답
    
    2-2 없다면?(신규유저이면)
    - 회원가입 진행 및 해당 유저의 JWT 발급
    - 그러나 도중에 예기치 못한 오류 발생시, 에러 메시지와 함께 오류 Status 응답
    """
    permission_classes = (AllowAny, )
    
    def get(self, request, *args, **kwargs):
        
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET
        code = request.GET.get('code')
        google_callback_uri = main_domain + "/accounts/google/callback",
        state = settings.STATE
        """
        Access Token Request
        """
        # 1. 해당 data를 넘긴다. -> 2. Token을 요청한다.
        data = {
                'grant_type': 'authorization_code',
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': google_callback_uri,
                'code': code
            }
        # 2. 해당 data를 Post하여 -> Token요청(현재 문제지점 -> 로그인 후 -> callback에서 오류가 걸림-> 찾아보는 중)
        token_req = requests.post("https://oauth2.googleapis.com/token", data=data)
        #token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={google_callback_uri}&state={state}")
        token_req_json = token_req.json()
        error = token_req_json.get('error', None)
            
        if error is not None:
            raise JSONDecodeError(error)
        # 3. 인가가능한 Token을 받아와서, 해당 유저의 info_response를 request
        access_token = token_req_json.get('access_token')
        """
        Email Request
        """
        email_req = requests.get(
            f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
        email_req_status = email_req.status_code
        if email_req_status != 200:
            return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
        email_req_json = email_req.json()
        email = email_req_json.get('email')
        """
        SignUp or Signin Request
        """
        try:
            user = User.objects.get(email=email)
            # 기존에 가입된 유저의 Provider가 Google이 아니면 에러 발생, 맞으면 로그인
                
            # 다른 SNS로 가입된 유저
            social_user = SocialAccount.objects.get(user=user)
            if social_user is None:
                return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
            if social_user.provider != 'google':
                return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
                
            # 기존에 Google로 가입된 유저
            p_data = {'access_token': access_token, 'code': code}
            accept = requests.post(
                    f"{main_domain}/accounts/google/login/success", data=p_data
                )
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
            accept_json = accept.json()
            return JsonResponse(accept_json)
        except User.DoesNotExist:
            # 기존에 가입된 유저가 없을 경우 새로 가입 진행
            p_data = {'access_token': access_token, 'code': code}
            accept = requests.post(
                f"{main_domain}/accounts/google/login/success", data=p_data) 
            return Response(accept.json(), status=status.HTTP_200_OK)
      
class GoogleToDjangoLoginView(SocialLoginView):
    adapter_class = google_views.GoogleOAuth2Adapter
    client_class = OAuth2Client       
            
                  
    
        
        
    