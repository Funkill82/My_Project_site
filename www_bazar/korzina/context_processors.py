from .korzina import Korzina


def korzina(request):
    """это функция, которая получает объект запроса в качестве параметра
     и возвращает словарь объектов, которые будут доступны всем шаблонам,
      визуализированным с помощью RequestContext."""
    return {'korzina': Korzina(request)}