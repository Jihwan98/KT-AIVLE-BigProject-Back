from rest_framework import serializers
from .models import Hospital, Pet

class  HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"
        
class  PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"