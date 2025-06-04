import requests
import time
from decimal import Decimal
from django.core.cache import cache
from currency_app.models import CurrencyRate
import logging

logger = logging.getLogger(__name__)


class CurrencyService:
    API_URL = "https://api.currencyapi.com/v3/latest"
    API_KEY = "cur_live_pHGk9A4RNsVWgrodC6U7VQKPDvDNEH7dGvz34KZC"
    CACHE_KEY = "last_currency_request"
    MIN_INTERVAL = 10  # в секундах

    @classmethod
    def get_usd_to_rub_rate(cls):
        """
        Получает текущий курс USD/RUB с API
        """
        last_request_time = cache.get(cls.CACHE_KEY)
        current_time = time.time()

        if last_request_time and (current_time - last_request_time) < cls.MIN_INTERVAL:
            latest_rate = CurrencyRate.objects.first()
            if latest_rate:
                return latest_rate.rate
            else:
                raise Exception("No cached rate available and too early for new request")

        try:
            params = {
                "apikey": cls.API_KEY,
                "base_currency": "USD",
                "currencies": "RUB",
            }

            response = requests.get(cls.API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            rub_data = data.get("data", {}).get("RUB")
            if not rub_data:
                raise Exception("RUB rate not found in API response")

            rate_value = rub_data.get("value")
            if rate_value is None:
                raise Exception("RUB rate is missing in response")

            # Сохраняем в базу данных
            rate_obj = CurrencyRate.objects.create(
                rate=Decimal(str(rate_value)),
                source="currencyapi.com"
            )

            cache.set(cls.CACHE_KEY, current_time, timeout=300)
            logger.info(f"Fetched USD/RUB rate: {rate_value}")
            return rate_obj.rate

        except requests.RequestException as e:
            logger.error(f"Error fetching from currencyapi.com: {e}")
            latest_rate = CurrencyRate.objects.first()
            if latest_rate:
                return latest_rate.rate
            raise Exception("API unavailable and no cached rate available")

    @classmethod
    def get_last_10_requests(cls):
        return CurrencyRate.objects.all().order_by('-timestamp')[:10]
