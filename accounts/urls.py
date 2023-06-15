from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    NaverLoginAPIView, NaverCallbackAPIView, NaverToDjangoLoginView
    )


app_name="accounts"
urlpatterns = [
    # path("register/", RegisterAPIView.as_view()), # post - 회원가입
    # path("auth/", AuthAPIView.as_view()), # post - 로그인, delete - 로그아웃, get - 유저정보
    # path("auth/refresh/", TokenRefreshView.as_view()), # jwt 토큰 재발급
    
    # 일반 회원 회원가입/로그인
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    # Naver Login
    path('naver/login',NaverLoginAPIView.as_view()),
    path('naver/callback', NaverCallbackAPIView.as_view()),
    path('naver/login/success', NaverToDjangoLoginView.as_view()),
    
    # Kakao Login
    # path('kakao/login', KakaoLoginAPIView.as_view()),
    # path('kakao/callback/', KakaoCallbackAPIView.as_view()),
    # path('kakao/login/success', KakaoToDjangoLoginView.as_view()),
    
    # Google Login
    path('google/login', GoogleLoginAPIView.as_view()),
    path('google/callback', GoogleCallbackAPIView.as_view()),
    path('google/login/success', GoogleToDjangoLoginView.as_view())
]

#https://nid.naver.com/oauth2.0/authorize?response_type=code&state=NAVER_LOGIN_STRING&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fuser%2Fnaver%2Fcallback&client_id=Qd5paRgcxlgMxClKlirF&oauth_os=&inapp_view=&locale=ko_KR