# ===== Инструкции по запуску =====

1. Создайте виртуальное окружение:
   python -m venv currency_env
   source currency_env/bin/activate  # Linux/Mac
   currency_env\Scripts\activate     # Windows

2. Установите зависимости:
   pip install -r requirements.txt

3. Создайте миграции и примените их:
   python manage.py makemigrations
   python manage.py migrate

4. Создайте суперпользователя (опционально):
   python manage.py createsuperuser

5. Запустите сервер:
   python manage.py runserver

6. Тестируйте API:
   curl http://localhost:8000/get-current-usd/
   
   или откройте в браузере:
   http://localhost:8000/get-current-usd/
7. Пример вывода:
   {
    "current_rate": {
        "currency_pair": "USD/RUB",
        "rate": 78.9107813558,
        "timestamp": "2025-06-04T17:03:58.506207+00:00"
    },
    "last_10_requests": [
        {
            "rate": 78.9108,
            "timestamp": "2025-06-04T17:03:58.506207+00:00",
            "source": "currencyapi.com"
        },
        {
            "rate": 78.9108,
            "timestamp": "2025-06-04T15:07:18.203004+00:00",
            "source": "currencyapi.com"
        },
        {
            "rate": 78.9108,
            "timestamp": "2025-06-04T15:06:17.284409+00:00",
            "source": "currencyapi.com"
        },
        {
            "rate": 78.9108,
            "timestamp": "2025-06-04T15:04:38.763728+00:00",
            "source": "currencyapi.com"
        }
    ],
    "status": "success"
    }