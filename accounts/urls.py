from django.urls import path
from . import views

app_name="accounts"
urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="Signup"),
    path("login/", views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # oauth2
    path("naverLogin/", views.NaverInfoView.as_view(), name='naver_login' ),
    path("naverLogout/", views.NaverLogoutView.as_view(), name='naver_logout')
    
    
]