# Django
from django import template
register = template.Library()

@register.inclusion_tag('templatetags/cart.html')
def cart(request):
    try:
        cart = request.session['cart']
    except KeyError:
        cart = []
    return {'cart': cart, 'request': request}

@register.filter()
def int_to_range(min = 0):
    return range(min)