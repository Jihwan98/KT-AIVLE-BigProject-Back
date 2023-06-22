from django.urls import path, include
from .views import *
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework.routers import DefaultRouter
from accounts.views import (
    NaverLoginAPIView, NaverCallbackAPIView, NaverToDjangoLoginView
    )
from django.views.generic import TemplateView
from django_pydenticon.views import image as pydenticon_image

router = DefaultRouter()
router.register('hospital', HospitalViewSet)
router.register('pet', PetViewSet)

urlpatterns = [
    # 일반 회원 회원가입/로그인
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')), # 회원가입
    path('user/delete/', DeleteAccount.as_view()), # 유저 삭제
    path('email/check/', EmailCheckAPIView.as_view()), # 이메일 중복 체크

    # 비밀번호 reset
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password/reset/confirm/<str:uidb64>/<str:token>', TemplateView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),

    # Naver Login
    path('naver/login',NaverLoginAPIView.as_view()),
    path('naver/callback', NaverCallbackAPIView.as_view()),
    path('naver/login/success', NaverToDjangoLoginView.as_view()),
    path('api/', include(router.urls)),
    
    # Kakao Login
    # path('kakao/login', KakaoLoginAPIView.as_view()),
    # path('kakao/callback/', KakaoCallbackAPIView.as_view()),
    # path('kakao/login/success', KakaoToDjangoLoginView.as_view()),
    
    # Google Login
    path('google/login', GoogleLoginAPIView.as_view()),
    path('google/callback', GoogleCallbackAPIView.as_view()),
    path('google/login/success', GoogleToDjangoLoginView.as_view()),

    # pydenticon
    path('identicon/image/<path:data>/', pydenticon_image, name='pydenticon_image'),]

#https://nid.naver.com/oauth2.0/authorize?response_type=code&state=NAVER_LOGIN_STRING&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fuser%2Fnaver%2Fcallback&client_id=Qd5paRgcxlgMxClKlirF&oauth_os=&inapp_view=&locale=ko_KR