from rest_framework import serializers
from .models import *
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
    profile_img = serializers.ImageField(default='profile/default.png')
    def get_cleaned_data(self):
        data = super().get_cleaned_data() # username, password, email 이 디폴트
        data['first_name'] = self.validated_data.get('first_name', '')
        data['is_vet'] = self.validated_data.get('is_vet', '')
        data['profile_img'] = self.validated_data.get('profile_img', '')

        return data

# 사용자 정보 추출
class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'is_vet', 'profile_img')

class  HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"
    
    # 생성시에는 user에 접근하여 ownerid에 값을 넣도록
    def create(self, validated_data):
        validated_data["user_id"] = self.context['request'].user
        hos = Hospital.objects.create(**validated_data)
        hos.save()
        return hos
        
class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        
        # 수정시 owner_id 수정 못하도록 필드 제한
        fields = ["id", "name", "species", "birth", "gender", "is_neu", "adoption_date"]
    
    # 생성시에는 user에 접근하여 ownerid에 값을 넣도록
    def create(self, validated_data):
        validated_data["ownerid"] = self.context['request'].user
        pet = Pet.objects.create(**validated_data)
        pet.save()
        return pet
    
class UserdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id' ,'email', 'first_name', 'is_vet', 'avatar']
        read_only_fields = ['id' ,'email', 'first_name', 'is_vet', 'avatar']