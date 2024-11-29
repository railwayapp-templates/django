# views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Supplies, SuppliesOrder, OrderItem
from .serializers import SuppliesSerializer, SupplyOrdersSerializer, SupplyOrderItemsSerializer

class SuppliesViewSet(viewsets.ModelViewSet):
    queryset = Supplies.objects.all()
    serializer_class = SuppliesSerializer
    permission_classes = [IsAuthenticated]

class SupplyOrdersViewSet(viewsets.ModelViewSet):
    queryset = SuppliesOrder.objects.all()
    serializer_class = SupplyOrdersSerializer
    permission_classes = [IsAuthenticated]

class SupplyOrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = SupplyOrderItemsSerializer
    permission_classes = [IsAuthenticated]

