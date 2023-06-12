from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# http -f POST http://localhost:8000/accounts/signup/ username=[username] password="[password]" 로 요청 가능
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # address 추가
    address = serializers.CharField()

    # validated_data 유효시 반환
    def create(self, validated_data):
        user = User.objects.create(username=validated_data["username"])
        user.address = validated_data["address"] 
        # password 암호화 후 저장
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ["pk", "username", "password", "address"]
        
class LoginSerialzier(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = CustomUser.objects.get(email=email)
    
        if not user.check_password(password):
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')

        return user
    
class NaverLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()