from django import template
register = template.Library()

@register.filter(name='dict_value_or_null')
def dict_value_or_null(dict, key):
    if key in dict:
        return dict[key]
    else:
        return 'null'

@register.filter(name='list_value_or_null')
def list_value_or_null(values_list, key):
    if len(values_list) == 4:
        return values_list[key]
    else:
        return 'null'
