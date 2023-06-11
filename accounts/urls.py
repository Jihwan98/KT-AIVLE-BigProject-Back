from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
	TokenVerifyView
)

app_name="accounts"
urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="login"),
    
    # TokenObtainPairView : access/refresh token 발급
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # TokenRefreshView : refresh token으로 access token 재발급
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # TokenVerifyView : 클라이언트가 서버 signing key 없이 HMAC-signed 토큰 검증
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]