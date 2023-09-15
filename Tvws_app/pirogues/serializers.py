from rest_framework import serializers
from .models import *

class PirogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pirogue
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'
