from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def query_update(context, **kwargs):
    """Скопировать текущий GET и переопределить/удалить ключи (None или '' удаляют)."""
    request = context["request"]
    q = request.GET.copy()
    for key, value in kwargs.items():
        if value is None or value == "":
            q.pop(key, None)
        else:
            q[key] = str(value)
    return q.urlencode()
