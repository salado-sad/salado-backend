from rest_framework import serializers
from .models import SaladoUser

class SaladoUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = SaladoUser
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'national_code',
        ]

    def create(self, validated_data):
        user = SaladoUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            date_of_birth=validated_data.get('data_of_brith', None),
            phone_number=validated_data.get('phone_number', ''),
            national_code=validated_data.get('national_code', '')
        )
        return user
