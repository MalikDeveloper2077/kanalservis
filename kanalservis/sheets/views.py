from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import OrderSerializer
from .services.orders import update_orders_from_google_sheet


class OrderAPIView(APIView):
    def get(self, _):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        update_orders_from_google_sheet()  # обновление данных БД
        return Response(serializer.data)
