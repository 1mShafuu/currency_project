from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from currency_app.services import CurrencyService
from currency_app.schemas import CurrencyAPIResponse, APIErrorResponse
import logging
from pydantic import ValidationError

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

        # Формируем данные ответа для текущего курса
        current_rate_data = {
            "currency_pair": "USD/RUB",
            "rate": float(current_rate),
            "timestamp": last_requests[0].timestamp.isoformat() if last_requests else None,
            "source": last_requests[0].source if last_requests else None
        }

        # Формируем данные для ответа за последние 10 запросов
        last_requests_data = [
            {
                "rate": float(req.rate),
                "timestamp": req.timestamp.isoformat(),
                "source": req.source
            }
            for req in last_requests
        ]

        # Валидируем ответ через Pydantic
        try:
            response_schema = CurrencyAPIResponse(
                current_rate=current_rate_data,
                last_10_requests=last_requests_data,
                status="success"
            )
            response_data = response_schema.dict()
        except ValidationError as e:
            logger.error(f"Response validation error: {e}")
            # Возвращаем упрощенный ответ в случае ошибки валидации
            response_data = {
                "current_rate": current_rate_data,
                "last_10_requests": last_requests_data,
                "status": "success"
            }

        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"Error in get_current_usd view: {e}")

        # Валидируем ошибку через Pydantic
        try:
            error_schema = APIErrorResponse(
                status="error",
                message=str(e),
                error_code="CURRENCY_FETCH_ERROR"
            )
            error_data = error_schema.dict()
        except ValidationError:
            # Fallback в случае ошибки валидации
            error_data = {
                "status": "error",
                "message": str(e)
            }

        return JsonResponse(error_data, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def service_info(request):
    """
    Endpoint для получения информации о конфигурации сервиса
    """
    try:
        info = CurrencyService.get_service_info()
        return JsonResponse({
            "status": "success",
            "service_info": info
        })
    except Exception as e:
        logger.error(f"Error getting service info: {e}")
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)
