from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

app_name="accounts"
urlpatterns = [
    # path("register/", RegisterAPIView.as_view()), # post - 회원가입
    # path("auth/", AuthAPIView.as_view()), # post - 로그인, delete - 로그아웃, get - 유저정보
    # path("auth/refresh/", TokenRefreshView.as_view()), # jwt 토큰 재발급
    
    # 일반 회원 회원가입/로그인
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
]