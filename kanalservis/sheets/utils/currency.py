from typing import Union

import requests


def get_rub_usd_rate():
    """Курс ЦБ РФ"""
    return requests.get(
        'https://www.cbr-xml-daily.ru/daily_json.js'
    ).json()['Valute']['USD']['Value']


def from_usd_to_rub(usd_price) -> Union[int, float]:
    usd_rate = get_rub_usd_rate()
    return round(usd_price * usd_rate, 2)