from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='addid')
def addid(value, arg):
    return value.as_widget(attrs={'id': arg})
  
@register.filter(name='addrows')
def addrows(value, arg):
    return value.as_widget(attrs={'rows': arg})
  
@register.filter(name='addcols')
def addcols(value, arg):
    return value.as_widget(attrs={'cols': arg})
  



@register.filter(name='get_class')
def get_class(value):
  return value.__class__.__name__
