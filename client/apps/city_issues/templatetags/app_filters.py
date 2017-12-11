from urllib import urlencode

from django import template

register = template.Library()

@register.simple_tag
def update_url(val, **kwargs):
    parameters = val.copy()
    if kwargs.get('order_by') == parameters.get('order_by') and parameters.get('reverse') != 'v_v':
        kwargs['reverse'] = 'v_v'
    elif kwargs.get('order_by') == parameters.get('order_by') and parameters.get('reverse') == 'v_v':
        kwargs['reverse'] = ''
    parameters.update(kwargs)
    return '?' + urlencode(parameters)
