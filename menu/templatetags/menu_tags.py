from django import template
from django.http import HttpResponse
from django.urls import reverse

from ..models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    menu_items = MenuItem.objects.filter(menu__name=menu_name).prefetch_related('children')
    current_url = context['request'].path
    menu_html = ''

    def build_menu(menu_item):
        nonlocal menu_html
        for item in menu_item:
            active = current_url == item.url or current_url.startswith(item.url + '/')
            children = item.children.all()
            has_children = children.exists()
            menu_html += f'<li class="{"active" if active else ""} {"has-children" if has_children else ""}">'
            if item.url:
                url = item.url
            else:
                url = reverse(item.name)
            menu_html += f'<a href="{url}">{item.title}</a>'
            if has_children:
                menu_html += '<ul>'
                build_menu(children)
                menu_html += '</ul>'
            menu_html += '</li>'

    build_menu(menu_items)
    return menu_html
