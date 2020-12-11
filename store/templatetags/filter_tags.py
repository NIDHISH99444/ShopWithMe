from django import template
register=template.Library()

 
@register.simple_tag
def selected_atribute(request_slug, slug):
    if request_slug==slug : 
        return "selected"
    else:
        return ""