# views.py

from rest_framework import viewsets
from .models import Supplies
from .serializers import SuppliesSerializer

class SuppliesViewSet(viewsets.ModelViewSet):
    queryset = Supplies.objects.all()
    serializer_class = SuppliesSerializer