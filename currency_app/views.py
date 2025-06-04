from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from currency_app.services import CurrencyService
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET"])
def get_current_usd(request):
    """
    API endpoint для получения текущего курса USD/RUB и истории последних 10 запросов
    """
    try:
        # Получаем текущий курс
        current_rate = CurrencyService.get_usd_to_rub_rate()

        # Получаем последние 10 запросов
        last_requests = CurrencyService.get_last_10_requests()

        # Формируем ответ
        response_data = {
            "current_rate": {
                "currency_pair": "USD/RUB",
                "rate": float(current_rate),
                "timestamp": last_requests[0].timestamp.isoformat() if last_requests else None
            },
            "last_10_requests": [
                {
                    "rate": float(req.rate),
                    "timestamp": req.timestamp.isoformat(),
                    "source": req.source
                }
                for req in last_requests
            ],
            "status": "success"
        }

        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"Error in get_current_usd view: {e}")
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)