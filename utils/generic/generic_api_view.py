from rest_framework import mixins, viewsets


class CommonAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Базовый класс для обработки запросов по API. (Класс для определения новых методов)
    """

    # Словарь с сериализаторами для запроса и ответа.
    # Пример: {'create': {'request': Serializer, 'response': Serializer}}
    # По умолчанию используется serializer_class
    SERIALIZER = {}
    lookup_field = "id"


class GenericAPIView(CommonAPIView):
    """
    Класс для обработки запросов по API. (Класс для переопределения методов DRF)
    """

    def get_serializer_class(self):
        """Возвращает класс сериализатора для запроса"""

        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )

        if self.action not in self.SERIALIZER:
            return self.serializer_class

        return self.SERIALIZER.get(self.action).get("request", self.serializer_class)

    def get_serializer_response(self, instance, **kwargs) -> dict:
        """Возвращает сериализованный объект"""

        if self.action not in self.SERIALIZER:
            return self.serializer_class(instance, **kwargs).data

        return self.SERIALIZER.get(self.action).get("response", self.serializer_class)(instance, **kwargs).data
