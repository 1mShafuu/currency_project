from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class CurrencyAPISettings(BaseSettings):
    """
    Настройки для работы с API валют
    """
    # API настройки
    api_key: Optional[str] = Field(default=None, description="API ключ для доступа к курсам валют")
    api_url: str = Field(default="https://api.exchangerate-api.com/v3/latest/", description="Базовый URL API")
    api_timeout: int = Field(default=10, description="Таймаут запросов к API в секундах")
    request_timeout: int = Field(default=10, description="Таймаут для HTTP запросов в секундах")
    max_retries: int = Field(default=3, description="Максимальное количество повторных попыток запроса")
    retry_delay: int = Field(default=1, description="Задержка между повторными попытками в секундах")
    rate_limit_delay: int = Field(default=60, description="Задержка при превышении лимита запросов в секундах")
    min_request_interval: int = Field(default=10,
                                      description="Минимальный интервал между запросами в секундах")

    # Django настройки
    debug: bool = Field(default=False, description="Режим отладки")
    secret_key: str = Field(description="Секретный ключ Django")

    # Настройки кэширования
    currency_cache_timeout: int = Field(default=300, description="Время жизни кэша курсов в секундах")
    cache_timeout: int = Field(default=300, description="Общий таймаут кэша в секундах")
    currency_min_request_interval: int = Field(default=10,
                                               description="Минимальный интервал между запросами в секундах")

    # Настройки валют по умолчанию
    default_base_currency: str = Field(default="USD", description="Базовая валюта по умолчанию")
    default_target_currency: str = Field(default="RUB", description="Целевая валюта по умолчанию")

    # Настройки логирования
    log_level: str = Field(default="INFO", description="Уровень логирования")
    log_requests: bool = Field(default=True, description="Логировать запросы к API")

    class Config:
        # Разрешаем дополнительные поля из переменных окружения
        extra = "allow"
        # Файл с переменными окружения
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Преобразование типов из строк
        case_sensitive = False


currency_settings = CurrencyAPISettings()
