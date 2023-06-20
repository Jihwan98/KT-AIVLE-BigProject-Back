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
        email = request.data.get('email')
        if User.objects.filter(email=email).exists(): # 이미 DB에 해당 email이 존재
            return JsonResponse({"success": False, "message" : "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else: # 생성가능
            return JsonResponse({"success": True, "message" : "Available emails"}, status=status.HTTP_200_OK)

# accounts/api/hospital     
class HospitalViewSet(ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(user_id=self.request.user)
        return queryset

# accounts/api/pet 
class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(ownerid=self.request.user)
        return queryset

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
            name = user_info["name"] # 사용자 이름
            

            # User 의 email 을 받아오지 못한 경우
            if email is None:
                return JsonResponse({
                    "error": "Can't Get Email Information from Naver"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(email=email, first_name=name)
                data = {'access_token': access_token, 'code': code, 'user': user}
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


# # 카카오 로그인 요청 ~ 인가코드 req & res
# class KakaoLoginAPIView(APIView):
#     """
#     1. 카카오 로그인 요청 -> 사용자 동의 -> 인가 코드 발급 요청
#     - 인가코드 = 토큰 받기에 필요한 값, 토큰에 부여할 권한 정보를 포함
#     2. 카카오 인증 서버는 해당 사용자에게 인가 코드를 발급
#     -> 인가 코드의 요청에 대한 응답 = redirect_uri = HTTP 302 Redirect
#     -> 해당 Location에 인가 코드가 담긴 쿼리 스트링을 포함
#     """
#     permission_classes = (AllowAny, )
    
#     def get(self, request):
#         # settings_param.py에 등록해둔 rest_api_key와 redirect_uri
#         client_id = "0e1fa375bb3d9b356f7ec7213157ccb0"
#         response_type = "code"
#         uri = main_domain + "/accounts/kakao/callback"
#         state = settings.STATE
#         kakao_url = "https://kauth.kakao.com/oauth/authorize?response_type=code"
#         return redirect(
#             f"{kakao_url}&client_id={client_id}&redirect_uri={uri}"
#             )
        
# # 토큰 받기 요청
# class KakaoCallbackAPIView(APIView):
#     """
#     1. 인가 코드를 활용해 토큰 발급 요청
#     2. 토큰 발급 요청이 끝나면 카카오 로그인이 정상적으로 완료 가능
#     """
#     permission_classes = (AllowAny, )
    
#     def get(self, request):
#         """
#         (1). Access Token Request
#         """
        
#         kakao_token_api = "https://kauth.kakao.com/oauth/token"
#         data = {
#             "grant_type"  : "authorization_code",
#             "client_id"   : "0e1fa375bb3d9b356f7ec7213157ccb0",
#             "redirect_uri": main_domain + "/accounts/kakao/callback",
#             "code"        : request.GET.get("code")
#         }
        
#         access_token = requests.post(kakao_token_api, data=data).json().get('access_token')
#         refresh_token = requests.post(kakao_token_api, data=data).json().get('refresh_token')
#         return JsonResponse({"token": access_token})
#         id_token = requests.post(kakao_token_api, data=data).json().get('id_token')
#         """
#         (2). 발급받은 토큰을 이용해서 GET 요청 
#         """
#         user_info = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f"Bearer {access_token}"}).json()
        
#         # return JsonResponse({"user_info": user_info})
        
#         """
#         (3) 1.전달 받은 사용자 정보를 이용해서, 내가 원하는 형태로 저장할 수 있도록 변수를 설정
#             2.DB에 원하는 정보가 없다면 저장, 정보가 이미 존재하면 바로 로그인(토큰 발급)
#         """
#         # 우리 DB: first_name, last_name, email, 
        
#         # kakao_acount = user_info.get("kakao_account")
#         #kakao_email = kakao_acount.get("email")
#         # kakao_id = kakao_acount.get("id")
#         #kakao_name = kakao_acount["profile"].get('nickname')
        
#         #return JsonResponse({"kakao": kakao_acount})
        
#         #kakao_id = user_info["id"] # 카카오 ID
#         #kakao_name = user_info["properties"]["nickname"] # 카카오 닉네임은 대부분 이름으로 설정하는 경우가 많음
#         #kakao_name = user_info["name"]
#         #kakao_email = user_info.get("email")  # 카카오 이메일
#         #kakao_name = user_info["kakao_account"].name_needs_agreement
#         #profile_image_url = user_info["properties"]["profile_image"]: 카톡 프사
        
#         # if kakao_email is None:
#         #     return JsonResponse({
#         #         "error": "Can't get Email information"
#         #     }, status=400)
#         # try:
#         #     user = User.objects.get(email=kakao_id)
#         #     data = {'access_token': access_token, "code": request.GET.get('code')}
#         #     accept = requests.post(
#         #         f"{main_domain}/accounts/kakao/login/success"
#         #     )
#         #     if accept.status_code != 200:
#         #             return JsonResponse({"error": "Failed to Signin."}, status=accept.status_code)
#         #     return Response(accept.json(), status=status.HTTP_200_OK)
#         # except User.DoesNotExist:
#         #     data = {'access_token': access_token, 'code': request.GET.get('code')}
#         #     accept = requests.post(
#         #             f"{main_domain}/accounts/naver/login/success", data=data
#         #         )
#         #     # token 발급
#         #     return Response(accept.json(), status=status.HTTP_200_OK)
    
            
            
            
           
#             #firstname에만 이름으 다 넣는 식으로
        
            
# class KakaoToDjangoLoginView(SocialLoginView):
#     adapter_class = kakao_views.KakaoOAuth2Adapter
#     client_class = OAuth2Client
#     callback_url = settings.KAKAO_REDIRECT_URI
    




class GoogleLoginAPIView(APIView):
    permission_classes = [
    	AllowAny,
    ]

    def get(self, request):
        GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID

        local_callback_uri = f"{main_domain}accounts/google/callback"

        google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"
        scope = (
            "https://www.googleapis.com/auth/userinfo.email "
            
        )
        redirect_uri = f"{google_auth_api}?client_id={GOOGLE_CLIENT_ID}&response_type=code&redirect_uri={local_callback_uri}&scope={scope}"
        return redirect(redirect_uri)






class GoogleCallbackAPIView(APIView):
    permission_classes = [
    	AllowAny,
    ]

    def get(self, request):
        code = request.GET.get("code")
        google_token_api = "https://oauth2.googleapis.com/token"
        GOOGLE_CLIENT_ID = '375584534650-k59r41tkahfjikkq2r3qod42bis6851d.apps.googleusercontent.com'
        GOOGLE_SECRET = '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'

        local_callback_uri = f"{main_domain}accounts/google/callback"

        state = "random_string"

        grant_type = "authorization_code"
        google_token_api += f"?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_SECRET}&code={code}&grant_type={grant_type}&&redirect_uri={local_callback_uri}&state={state}"
        token_response = requests.post(google_token_api)

        
        if not token_response.ok:
            raise ValueError("google_token is invalid")

        access_token = token_response.json().get("access_token")

        #return JsonResponse({"access_token": access_token})
        # 구글 프로필 정보 가져오기
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            params={"access_token": access_token},
        )

        if not user_info.ok:
            raise ValueError("사용자 정보를 불러오는데 실패했습니다.")

        user_info_json = user_info.json()
        #return JsonResponse({"user_info": user_info_json})
        # 사용자 이름
        #username = user_info_json.get('name')
        email = user_info_json.get('email')
        
        try:
                user = User.objects.get(email=email)
                data = {'access_token': access_token, 'code': code}
                # accept 에는 token 값이 json 형태로 들어온다({"key"}:"token value")
                # 여기서 오는 key 값은 authtoken_token에 저장된다.
                
                
                accept = requests.post(
                    f"{main_domain}/accounts/google/login/success", data=data
                )
                # 만약 token 요청이 제대로 이루어지지 않으면 오류처리
                #if accept.status_code != 200:
                    #return JsonResponse({"error": "Failed to Signin."}, status=accept.status_code)
                return Response(accept.json(), status=status.HTTP_200_OK)

        except User.DoesNotExist:
                # user = {
                    
                # }
                # user.save()
                data = {'access_token': access_token, 'code': code}
                accept = requests.post(
                    f"{main_domain}/accounts/google/login/success", data=data
                )
                # token 발급
                return Response(accept.json(), status=status.HTTP_200_OK)
                
        
            
            
            





# class GoogleCallbackAPIView(APIView):
#     """
#     1. 전달받은 email과 동일한 Email이 있는지 찾아본다.
#     2-1 만약 있다면?
#     - socialaccount(소셜로그인한) 테이블에서 해당 이메일의 유저가 있는지 체크
#     - 없으면 해당 계정은 일반계정(backend DB에 있는), 에러 메시지와 함께 400 리턴
#     - 위 두개에 걸리지 않으면 로그인 진행, 해당 유저의 JWT발급, 그러나 중간에 예기치 못한 오류가 발생하면 에러메시지와 함께 오류 Status응답
    
#     2-2 없다면?(신규유저이면)
#     - 회원가입 진행 및 해당 유저의 JWT 발급
#     - 그러나 도중에 예기치 못한 오류 발생시, 에러 메시지와 함께 오류 Status 응답
#     """
#     permission_classes = (AllowAny, )
    
#     def get(self, request, *args, **kwargs):
        
#             client_id = settings.GOOGLE_CLIENT_ID
#             client_secret = settings.GOOGLE_CLIENT_SECRET
#             code = request.GET.get('code')
#             google_callback_uri = main_domain + "/accounts/google/callback"
#             #state = settings.STATE
#             grant_type = 'authorization_code'
#             state = request.GET.get('state')
#             """
#             Access Token Request
#             """
#             # 1. 해당 data를 넘긴다. -> 2. Token을 요청한다.
#             data = {
#                     'grant_type': 'authorization_code',
#                     'client_id': client_id,
#                     'client_secret': client_secret,
#                     'redirect_uri': google_callback_uri,
#                     'code': code
#                 }
#             parameters = f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}&redirect_uri={google_callback_uri}"

#             #token_req = requests.post(f"https://oauth2.googleapis.com/token?{parameters}")
            
#             # 2. 해당 data를 Post하여 -> Token요청(현재 문제지점 -> 로그인 후 -> callback에서 오류가 걸림-> 찾아보는 중)
#             token_req = requests.post("https://oauth2.googleapis.com/token", data=data)
#             #token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={google_callback_uri}&state={state}")
#             token_req_json = token_req.json()
#             error = token_req_json.get('error', None)
                
#             if error is not None:
#                 raise JSONDecodeError(error)
#             # 3. 인가가능한 Token을 받아와서, 해당 유저의 info_response를 request
#             access_token = token_req_json.get('access_token')
#             """
#             Email Request
#             """
#             email_req = requests.get(
#                 f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
#             email_req_status = email_req.status_code
#             if email_req_status != 200:
#                 return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
#             email_req_json = email_req.json()
#             email = email_req_json.get('email')
#             """
#             SignUp or Signin Request
#             """
            
#             try:
#                 user = User.objects.get(email=email)
#                 data = {'access_token': access_token, 'code': code}
#                 # accept 에는 token 값이 json 형태로 들어온다({"key"}:"token value")
#                 # 여기서 오는 key 값은 authtoken_token에 저장된다.
#                 accept = requests.post(
#                     f"{main_domain}/accounts/google/login/success", data=data
#                 )
#                 # 만약 token 요청이 제대로 이루어지지 않으면 오류처리
#                 if accept.status_code != 200:
#                     return JsonResponse({"error": "Failed to Signin."}, status=accept.status_code)
#                 return Response(accept.json(), status=status.HTTP_200_OK)

#             except User.DoesNotExist:
#                 data = {'access_token': access_token, 'code': code}
#                 accept = requests.post(
#                     f"{main_domain}/accounts/google/login/success", data=data
#                 )
#                 # google API update되어서 해당 코드를 넣어줘야함.
#                 accept_json = accept.json()
#                 #accept_json.pop("user", None)
#                 # token 발급
#                 return Response(accept_json, status=status.HTTP_200_OK)
                
#         # except:
#         #     return JsonResponse({
#         #         "error": "error",
#         #     }, status=status.HTTP_404_NOT_FOUND)
            
#         #     try:
#         #         user = User.objects.get(email=email)
#         #         # 기존에 가입된 유저의 Provider가 Google이 아니면 에러 발생, 맞으면 로그인
                    
#         #         # 다른 SNS로 가입된 유저
#         #         social_user = SocialAccount.objects.get(user=user)
#         #         if social_user is None:
#         #             return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
#         #         if social_user.provider != 'google':
#         #             return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
                    
#         #         # 기존에 Google로 가입된 유저
#         #         p_data = {'access_token': access_token, 'code': code}
#         #         accept = requests.post(
#         #                 f"{main_domain}/accounts/google/login/success", data=p_data
#         #             )
#         #         accept_status = accept.status_code
#         #         if accept_status != 200:
#         #             return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
#         #         accept_json = accept.json()
#         #         return JsonResponse(accept_json)
#         #     except User.DoesNotExist:
#         #         # 혹은 회원가입 API를 써서 POST하는 방식으로 진행
#         #         # 기존에 가입된 유저가 없을 경우 새로 가입 진행
#         #         p_data = {'access_token': access_token, 'code': code}
#         #         # DB에 해당 정보를 저장하는 부분을 추가
                
#         #         accept = requests.post(
#         #             f"{main_domain}/accounts/google/login/success", data=p_data) 
#         #         return Response(accept.json(), status=status.HTTP_200_OK)
#         # # except
#         # #     return JsonResponse({
#         # #         "error": "error",
#         # #     }, status=status.HTTP_404_NOT_FOUND)
class GoogleToDjangoLoginView(SocialLoginView):
    adapter_class = google_views.GoogleOAuth2Adapter
    client_class = OAuth2Client 
    
# class CustomUserDetailsView(RetrieveUpdateAPIView):
#     # serializer_class = CustomUserDetailsSerializer
#     serializer_class = UserDetailsSerializer
    
#     def get(self, request, *args, **kwargs):
#         self.serializer_class = DetailsRetrieveSerializer
#         return super().get(request, *args, **kwargs)


    
    