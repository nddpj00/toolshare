from django import template

register = template.Library()

@register.filter
def insert_line_breaks(value):
    return value.replace('.', '.<br><br>')
