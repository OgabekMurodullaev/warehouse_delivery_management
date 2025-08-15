from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from warehouse.models import Warehouse
from warehouse.permissions import IsWarehouseManagerOrReadOnly
from warehouse.serializers import WarehouseSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsWarehouseManagerOrReadOnly]
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    @action(detail=True, methods=['get'])
    def capacity_check(self, request, pk=None):
        warehouse = self.get_object()
        total_quantity = sum(stock.quantity for stock in warehouse.stock_items.all())
        available_space = warehouse.capacity - total_quantity
        return Response({
            "capacity": warehouse.capacity,
            "user": total_quantity,
            "available": available_space
        })