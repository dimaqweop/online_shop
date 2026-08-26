from django import template

register = template.Library()


@register.filter(name='user_role')
def user_role(user):
    if getattr(user, 'is_staff', False):
        return "Адміністратор"
    return "Користувач"
