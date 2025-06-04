# Django Currency API

## Подзадачи

### 1. Настройка Django проекта
- Создание базового проекта и приложения  
- Настройка URL-маршрутизации

### 2. Создание модели данных
- Модель для хранения истории запросов курса  
- Миграции базы данных

### 3. Интеграция с внешним API
- Выбор и подключение API для получения курса валют  
- Обработка ошибок API

### 4. Реализация логики кэширования
- Контроль паузы между запросами (10+ секунд)  
- Кэширование последнего результата

### 5. Создание API endpoint
- View для обработки запроса `/get-current-usd/`  
- Возврат JSON с текущим курсом и историей

### 6. Тестирование и финализация

---

## ⚙️ Заполнение файла `.env`

Создайте файл `.env` в корне проекта и добавьте туда следующие переменные окружения:

- **CURRENCY_API_KEY** — ваш ключ доступа к внешнему API курса валют.  

- **CURRENCY_API_URL** — URL API для получения курса валют.  
  Пример: `https://api.currencyapi.com/v3/latest`

- **DEBUG** — режим отладки Django.  
  Значение: `True` или `False`

- **SECRET_KEY** — секретный ключ Django для обеспечения безопасности приложения.  

- **CURRENCY_CACHE_TIMEOUT** — время кэширования курса валют в секундах.  
  Пример: `300` (5 минут)

- **CURRENCY_MIN_REQUEST_INTERVAL** — минимальный интервал между запросами к внешнему API в секундах.  
  Пример: `10`

---

## Инструкции по запуску

### 1. Создайте виртуальное окружение:

    python -m venv currency_env  
    source currency_env/bin/activate        # Для Linux/Mac  
    currency_env\\Scripts\\activate         # Для Windows

### 2. Установите зависимости:

    pip install -r requirements.txt

### 3. Создайте миграции и примените их:

    python manage.py makemigrations  
    python manage.py migrate

### 4. Создайте суперпользователя (опционально):

    python manage.py createsuperuser

### 5. Запустите сервер:

    python manage.py runserver

### 6. Тестируйте API:

    #С помощью curl:  
    curl http://localhost:8000/get-current-usd/

    #Или откройте в браузере:  
    http://localhost:8000/get-current-usd/

### 7. Пример вывода:
```json
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
