from rest_framework import serializers
from .models import Hospital, Pet

class  HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"
        
class  PetSerializer(serializers.ModelSerializer):
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
        
            