from datetime import datetime
from typing import Union

from ..models import Order
from ..utils.orders import get_rub_usd_rate
from ..utils.sheets import get_google_service_sacc


SHEET_ID = '1X6wVZvoOBgY7QJWhtAaKeDpcH_8ZYerpwdjIvkN9Thg'

# Индексы колонок в данных от google sheet.
ORDER_NUMBER = 0
PRICE = 1
DELIVERY_DATE = 2

google_service = get_google_service_sacc()


def sheet_order_row_to_dict(sheet_order_row: list, usd_rate: Union[int, float] = get_rub_usd_rate()) -> dict:
    return {
        'order_number': sheet_order_row[ORDER_NUMBER],
        'usd_price': int(sheet_order_row[PRICE]),
        'rub_price': round(int(sheet_order_row[PRICE]) * usd_rate, 2),
        'delivery_date': datetime.strptime(sheet_order_row[DELIVERY_DATE], "%d.%m.%Y").strftime("%Y-%m-%d")
    }


def db_order_to_sheet_row(db_order):
    return [
        str(db_order.order_number),
        str(db_order.usd_price),
        datetime.strptime(str(db_order.delivery_date), '%Y-%m-%d').strftime('%d.%m.%Y')
    ]


def get_google_sheet_orders(spreadsheet_id: str):
    return google_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range='B2:D999'
    ).execute()['values']


class SheetOrderManager:
    """Абстрактный класс для работы с заказами из google sheets для БД"""
    db_orders_numbers = Order.objects.values_list('order_number', flat=True)

    def __init__(self, spreadsheet_id: str):
        self.sheet_orders = get_google_sheet_orders(spreadsheet_id)

    @property
    def sheet_orders_numbers(self):
        return [order[ORDER_NUMBER] for order in self.sheet_orders]

    def update_db(self):
        """Метод должен быть реализован в каждом дочернем классе.
        Подразумевает применение изменений (сути класса) в БД.
        """
        raise NotImplementedError


class SheetOrderCreateManager(SheetOrderManager):
    def get_new_sheet_orders(self):
        print(self.db_orders_numbers, self.sheet_orders)
        return list(filter(lambda order: int(order[ORDER_NUMBER]) not in list(Order.objects.values_list('order_number', flat=True)), self.sheet_orders))

    def update_db(self):
        print('new', self.get_new_sheet_orders())
        usd_rate = get_rub_usd_rate()
        return Order.objects.bulk_create([
            Order(**sheet_order_row_to_dict(sheet_order, usd_rate=usd_rate))
            for sheet_order in self.get_new_sheet_orders()
        ])


class SheetOrderDeleteManager(SheetOrderManager):
    def get_deleted_sheet_orders_numbers(self):
        return list(filter(
            lambda db_order_number: str(db_order_number) not in self.sheet_orders_numbers,
            self.db_orders_numbers
        ))

    def update_db(self):
        return Order.objects.filter(
            order_number__in=self.get_deleted_sheet_orders_numbers()
        ).delete()


class SheetOrderUpdateManager(SheetOrderManager):
    def get_updated_sheet_orders_numbers(self):
        """TODO return"""
        sorted_db_orders = Order.objects.all().order_by('order_number')
        sorted_sheet_orders = sorted(self.sheet_orders, key=lambda o: int(o[ORDER_NUMBER]))

        return [(db_order.order_number, sheet_order) for db_order, sheet_order in zip(
            sorted_db_orders, sorted_sheet_orders
        ) if db_order_to_sheet_row(db_order) != sheet_order]

    def update_db(self):
        updated_orders_numbers = self.get_updated_sheet_orders_numbers()
        for order_number, sheet_order in updated_orders_numbers:
            Order.objects.filter(order_number=order_number).update(**sheet_order_row_to_dict(sheet_order))


def update_orders_from_google_sheet():
    """Синхронизация данных БД и google sheets."""
    orders_actions_classes = (
        SheetOrderCreateManager(SHEET_ID),
        SheetOrderUpdateManager(SHEET_ID),
        SheetOrderDeleteManager(SHEET_ID)
    )

    for action_class in orders_actions_classes:
        action_class.update_db()
