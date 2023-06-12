from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import SignupSerializer
from rest_framework.views import APIView
# 로그인, 로그아웃
# JWT
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response

# OAuth2 로그인
from django.contrib.auth import logout as auth_logout


# naver oauth2
class NaverInfoView(APIView):
    
    
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            user_info = {
                'username': user.username,
                'address': user.address,
            }
            return Response(user_info)
        return Response({'detail': 'User not authenticated'})

class NaverLogoutView(APIView):
    def post(self, request):
        auth_logout(request)
        return Response({'detail': 'Logged out successful'})









class SignupView(CreateAPIView):
    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny,]
    
class LoginView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # JWT 토큰 생성
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            
            
            # 프론트엔드로 토큰 전달
            response_data = {
                'refresh_token': str(refresh_token),
                'access_token': access_token,
                'success': '로그인 되었습니다.'
            }
            print(request.user)
            print(request.auth)
            return Response(response_data)
            
        else:
            return Response({'error': '해당 정보가 없습니다.'})

        
        
        
class LogoutView(APIView):
    def post(self, request):
        return Response({'success': '로그아웃되었습니다.'})