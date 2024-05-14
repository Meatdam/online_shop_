from django import template

register = template.Library()


@register.filter(name='media_filter')
def media_filter(path) -> str:
    """
    Шаблоный фильтр для отображения коректного пути для изображения
    :return: str
    """
    if path:
        return f"/media/{path}"
    return "#"
