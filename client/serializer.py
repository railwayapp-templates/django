# serializers.py

from rest_framework import serializers
from .models import Client, AreaServiced

class AreaServicedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaServiced
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'