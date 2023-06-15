from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model

# 기본 유저 모델 불러오기
User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: email, password
    # 추가 설정 필드: is_vet
    first_name = serializers.CharField(required=True)
    is_vet = serializers.BooleanField(default=False)
    def get_cleaned_data(self):
        data = super().get_cleaned_data() # username, password, email 이 디폴트
        data['first_name'] = self.validated_data.get('first_name', '')
        data['is_vet'] = self.validated_data.get('is_vet', '')

        return data

# 사용자 정보 추출
class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'is_vet')