from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# http -f POST http://localhost:8000/accounts/signup/ username=[username] password="[password]" 로 요청 가능
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # validated_data 유효시 반환
    def create(self, validated_data):
        user = User.objects.create(username=validated_data["username"],
                                   email = validated_data['email'],
                                   first_name= validated_data['first_name'],
                                   last_name= validated_data['last_name'],
                                   )

        # password 암호화 후 저장
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        # fields = '__all__'
        fields = ["username", "password", 'email', 'first_name', 'last_name']