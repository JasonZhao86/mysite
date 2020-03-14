from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template.defaultfilters import urlize, linebreaksbr


register = template.Library()


@register.filter
@stringfilter
def cut(value, substr):
    return value.replace(substr, "")


# register.filter("cut", cut)


@register.filter(is_safe=True)
# @register.filter
@stringfilter
def add(value, substr):
    return "{}{}".format(value, substr)


@register.filter(needs_autoescape=True)
@stringfilter
def initial_letter_first(value, autoescape=None):
    first_frag = value[0]
    other_frag = value[1:]
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe("<strong>{}</strong>{}".format(esc(first_frag), esc(other_frag)))


@register.filter(expects_localtime=True)
# @register.filter
def businesshours(value):
    print(type(value))
    return value.hour


@register.filter
def urlize_and_linebreaksbr(value):
    return linebreaksbr(urlize(value, autoescape=True), autoescape=True)