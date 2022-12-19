from django import template
from store.models import *

register = template.Library()

all_icons = [
    '<i class="fa-solid fa-tree"></i>',
    '<i class="fa-solid fa-microchip"></i>',
    '<i class="fa-solid fa-glasses"></i>',
    '<i class="fa-solid fa-basketball"></i>',
    '<i class="fa-solid fa-book"></i>'
]

@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('store/list_categories.html')
def show_categories():
    icons = all_icons
    cats = Category.objects.all()
    return {'cats': cats, 'icons': icons}
