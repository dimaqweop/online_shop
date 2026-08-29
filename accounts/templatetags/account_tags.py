from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag
def days_on_site(date_joined):
    if not date_joined:
        return "перший день"

    now = timezone.now()
    delta = now - date_joined
    days = delta.days

    if days <= 0:
        hours = delta.seconds // 3600
        return f"{hours} год. тому" if hours > 0 else "щойно"

    if days % 10 == 1 and days % 100 != 11:
        return f"{days} день"
    elif days % 10 in [2, 3, 4] and days % 100 not in [12, 13, 14]:
        return f"{days} дні"
    else:
        return f"{days} днів"


@register.inclusion_tag('accounts/includes/user_badge.html')
def user_badge(user):
    return {'user': user}

