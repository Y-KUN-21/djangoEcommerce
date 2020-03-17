from django import template
from main.models import Order, OrderProduct

register = template.Library()


@register.filter
def cart_count(user):
    if user.is_authenticated:
        get_qs = Order.objects.filter(user=user, ordered=False)
        for item in get_qs:
            return get_qs[0].item.count()
        return 0
