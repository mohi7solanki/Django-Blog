from django import template
register = template.Library()


@register.filter
def get_name(value):
    spam = value.split('/')[-1]
    spam = ' '.join(spam.split('-'))
    return spam

