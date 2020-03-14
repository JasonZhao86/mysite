from django import template
from books.models import Book
import datetime

register = template.Library()


@register.simple_tag(takes_context=True, name="curtime")
def current_time(context, format_string):
    for i in context:
        if "csrf_token" in i:
            print(i["csrf_token"])
    return datetime.datetime.strftime(datetime.datetime.now(), format_string)


@register.inclusion_tag("authors.html")
def books_for_author(author):
    books = Book.objects.filter(authors__id=author.id)
    return {"books": books}


@register.inclusion_tag("messages.html", takes_context=True)
def get_messages(context):
    user = context["user"]
    ip_address = context["ip_address"]
    message = context["message"]
    return {"user": user, "ip_address": ip_address, "message": message}
