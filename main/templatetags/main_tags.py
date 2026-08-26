from django import template
from urllib.parse import quote

register = template.Library()


@register.inclusion_tag('main/components/share_buttons.html', takes_context=True)
def show_share_buttons(context, post_title):
    """
    Рендерить блок кнопок поширення статті/товару в соцмережах на основі поточної URL-адреси з контексту запиту.
    Використання в шаблоні: {% show_share_buttons product.name %}
    """
    request = context.get('request')
    absolute_url = request.build_absolute_uri() if request else ''

    return {
        'share_url': quote(absolute_url),
        'share_title': quote(str(post_title)),
        'raw_url': absolute_url,
    }
