from django import template

register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__[:-4]


@register.filter(name='remove_last')
def remove_last(value):
    return value + "hello"
