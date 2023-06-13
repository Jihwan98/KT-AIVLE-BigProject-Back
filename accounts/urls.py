from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from accounts.views import (
    NaverLoginAPIView, NaverCallbackAPIView, NaverToDjangoLoginView
    )

app_name="accounts"

router = DefaultRouter()
router.register('hospital', views.HospitalViewSet)
router.register('pet', views.PetViewSet)

urlpatterns = [    
    # 일반 회원 회원가입/로그인
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    # Naver Login
    path('naver/login',NaverLoginAPIView.as_view()),
    path('naver/callback', NaverCallbackAPIView.as_view()),
    path('naver/login/success', NaverToDjangoLoginView.as_view()),
    path('api/', include(router.urls))
]

#https://nid.naver.com/oauth2.0/authorize?response_type=code&state=NAVER_LOGIN_STRING&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fuser%2Fnaver%2Fcallback&client_id=Qd5paRgcxlgMxClKlirF&oauth_os=&inapp_view=&locale=ko_KR