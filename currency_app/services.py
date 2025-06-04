import requests
import time
from decimal import Decimal
from django.core.cache import cache
from currency_app.models import CurrencyRate
from currency_app.config import currency_settings
from currency_app.schemas import CurrencyRateData, CurrencyRateRequest
import logging
from typing import Optional
from pydantic import ValidationError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CurrencyService:
    """
    Сервис для работы с API курсов валют
    """

    CACHE_KEY = "last_currency_request"

    @classmethod
    def get_usd_to_rub_rate(cls) -> Decimal:
        """
        Получает текущий курс USD/RUB с учетом ограничения по времени
        """
        # Проверяем интервал между запросами
        # Добавьте в начало get_usd_to_rub_rate:
        logger.info(f"currency_min_request_interval = {currency_settings.currency_min_request_interval}")
        if not cls._can_make_request():
            latest_rate = CurrencyRate.objects.first()
            if latest_rate:
                logger.info("Returning cached rate due to rate limiting")
                return latest_rate.rate
            else:
                raise Exception("No cached rate available and too early for new request")

        cache.set(cls.CACHE_KEY, time.time(), timeout=currency_settings.cache_timeout)

        # Валидируем запрос
        try:
            request_data = CurrencyRateRequest(
                base_currency="USD",
                target_currency="RUB"
            )
        except ValidationError as e:
            logger.error(f"Request validation error: {e}")
            raise Exception(f"Invalid request parameters: {e}")

        # Получаем курс с API
        rate_value = cls._fetch_from_api(request_data)

        if rate_value is None:
            # Возвращаем кэшированный курс в случае ошибки API
            latest_rate = CurrencyRate.objects.first()
            if latest_rate:
                logger.warning("API unavailable, returning cached rate")
                return latest_rate.rate
            raise Exception("API unavailable and no cached rate available")

        # Валидируем и сохраняем данные
        try:
            rate_data = CurrencyRateData(
                rate=rate_value,
                source="currencyapi.com",
                timestamp=CurrencyRate._meta.get_field('timestamp').default()
            )
        except ValidationError as e:
            logger.error(f"Rate data validation error: {e}")
            raise Exception(f"Invalid rate data: {e}")

        # Сохраняем в базу данных
        rate_obj = CurrencyRate.objects.create(
            rate=rate_data.rate,
            source=rate_data.source
        )

        logger.info(f"Successfully fetched and saved USD/RUB rate: {rate_value}")
        return rate_obj.rate

    @classmethod
    def _can_make_request(cls) -> bool:
        """
        Проверяет, можно ли делать новый запрос к API
        """
        last_request_time = cache.get(cls.CACHE_KEY)
        if last_request_time is None:
            return True

        current_time = time.time()
        time_passed = current_time - last_request_time

        min_interval = currency_settings.currency_min_request_interval

        # Добавляем логирование для отладки
        logger.debug(f"Time passed: {time_passed:.2f}s, min interval: {min_interval}s")

        can_request = time_passed >= min_interval
        if not can_request:
            remaining_time = min_interval - time_passed
            logger.info(f"Rate limit active. Need to wait {remaining_time:.2f} more seconds")

        return can_request

    @classmethod
    def _fetch_from_api(cls, request_data: CurrencyRateRequest) -> Optional[Decimal]:
        """
        Делает запрос к API для получения курса валют
        """
        for attempt in range(currency_settings.max_retries):
            try:
                params = {
                    "apikey": currency_settings.currency_api_key,
                    "base_currency": request_data.base_currency,
                    "currencies": request_data.target_currency,
                }

                logger.info(f"Making API request (attempt {attempt + 1}/{currency_settings.max_retries})")

                response = requests.get(
                    str(currency_settings.currency_api_url),
                    params=params,
                    timeout=currency_settings.request_timeout,
                    headers={
                        'User-Agent': 'Django-Currency-Service/1.0',
                        'Accept': 'application/json'
                    }
                )
                response.raise_for_status()

                data = response.json()

                # Извлекаем курс из ответа
                currency_data = data.get("data", {}).get(request_data.target_currency)
                if not currency_data:
                    logger.error(f"{request_data.target_currency} rate not found in API response")
                    continue

                rate_value = currency_data.get("value")
                if rate_value is None:
                    logger.error(f"{request_data.target_currency} rate value is missing")
                    continue

                # Валидируем что курс положительный
                if rate_value <= 0:
                    logger.error(f"Invalid rate value: {rate_value}")
                    continue

                return Decimal(str(rate_value))

            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout (attempt {attempt + 1})")
                if attempt == currency_settings.max_retries - 1:
                    logger.error("All retry attempts exhausted due to timeouts")
                else:
                    time.sleep(1)

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error (attempt {attempt + 1}): {e}")
                if attempt == currency_settings.max_retries - 1:
                    logger.error("All retry attempts exhausted due to request errors")
                else:
                    time.sleep(1)

            except (ValueError, KeyError) as e:
                logger.error(f"Data parsing error (attempt {attempt + 1}): {e}")
                break

            except Exception as e:
                logger.error(f"Unexpected error (attempt {attempt + 1}): {e}")
                break

        return None

    @classmethod
    def get_last_10_requests(cls):
        """
        Возвращает последние 10 запросов курсов
        """
        return CurrencyRate.objects.all().order_by('-timestamp')[:10]

    @classmethod
    def get_service_info(cls) -> dict:
        """
        Возвращает информацию о конфигурации сервиса
        """
        return {
            "api_url": str(currency_settings.currency_api_url),
            "min_interval": currency_settings.currency_min_request_interval,
            "cache_timeout": currency_settings.cache_timeout,
            "request_timeout": currency_settings.request_timeout,
            "max_retries": currency_settings.max_retries,
            "api_key_configured": bool(currency_settings.currency_api_key)
        }