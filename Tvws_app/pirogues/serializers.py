from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from alertes.models import Alerte



class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = '__all__'



User = Pirogue

class PirogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pirogue
        fields = '__all__'
        
    extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email =validated_data['email'],
            # is_marine=validated_data['is_marine']
        )

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        validated_data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return validated_data


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


User = Pirogue

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom user data to the token response
        user = self.user
        data['id'] = user.id
        data['username'] = user.username
        data['email'] = user.email
        data['tel'] = user.tel

        return data

class ConnectedPositionSerializer(serializers.ModelSerializer):
    pirogue = serializers.PrimaryKeyRelatedField(queryset=Pirogue.objects.all())
    time_since_last_position = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = ('pirogue', 'latitude', 'longitude', 'timestamp', 'time_since_last_position')

    def get_time_since_last_position(self, obj):
        now = timezone.now()
        last_position_time = obj.timestamp
        return (now - last_position_time).total_seconds() / 60