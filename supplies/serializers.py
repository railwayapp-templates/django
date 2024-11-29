# serializers.py

from rest_framework import serializers
from .models import Supplies, SuppliesOrder, OrderItem

class SuppliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplies
        fields = '__all__'
    
class SupplyOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliesOrder
        fields = '__all__'

class SupplyOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'