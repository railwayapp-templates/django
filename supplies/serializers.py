# serializers.py

from rest_framework import serializers
from .models import Supplies

class SuppliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplies
        fields = '__all__'