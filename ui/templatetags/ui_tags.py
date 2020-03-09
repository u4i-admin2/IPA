from django import template
register = template.Library()


def addattr(field, input):
    items = input.split(',')
    attrs_dict = {}
    for item in items:
        parts = item.split(':')
        attrs_dict[parts[0]] = parts[1]
    return field.as_widget(attrs=attrs_dict)


register.filter('addattr', addattr)
