# survey/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from .models import ClientSurvey2024, ZipcodeSurvey, Surveyor, Survey
from .serializers import ClientSurvey2024Serializer, ZipcodeSurveySerializer, SurveyorSerializer, SurveySerializer

class ClientSurvey2024ViewSet(viewsets.ModelViewSet):
    queryset = ClientSurvey2024.objects.all()
    serializer_class = ClientSurvey2024Serializer
    permission_classes = [IsAuthenticated]

class ZipcodeSurveyViewSet(viewsets.ModelViewSet):
    queryset = ZipcodeSurvey.objects.all()
    serializer_class = ZipcodeSurveySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['zipcode']

class SurveyorViewSet(viewsets.ModelViewSet):
    queryset = Surveyor.objects.all()
    serializer_class = SurveyorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]
