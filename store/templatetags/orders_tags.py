from django import template
register=template.Library()

@register.simple_tag
def get_order_status_class(status ):
    if status=="COMPLETE":
        return "success"
    elif status=="PENDING":
        return "warning"
    else:
        return "info"