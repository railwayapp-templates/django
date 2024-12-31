# survey/serializers.py

from rest_framework import serializers
from .models import ClientSurvey2024, ZipcodeSurvey, Surveyor, Survey

class ClientSurvey2024Serializer(serializers.ModelSerializer):
    class Meta:
        model = ClientSurvey2024
        fields = '__all__'

class ZipcodeSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipcodeSurvey
        fields = '__all__'

class SurveyorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surveyor
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


