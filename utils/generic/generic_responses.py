from rest_framework.response import Response


def response_success(data: dict = None, status: int = 200) -> Response:
    """Возвращает стандартизированный успешный ответ."""

    return Response(data={"success": True, "data": data}, status=status)


def response_error(data: dict = None, status: int = 400, message: str = "Ошибка") -> Response:
    """Возвращает стандартизированный неуспешный ответ."""

    return Response(data={"success": False, "error_message": message, "data": data}, status=status)
