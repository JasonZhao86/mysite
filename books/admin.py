from django.contrib import admin
from .models import Author, Publisher, Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    search_fields = ("first_name", "last_name")

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "publication_date", "publisher")
    search_fields = ("title", "authors", "publisher")
    list_filter = ("publication_date", "publisher")
    date_hierarchy = "publication_date"
    ordering = ("-publication_date",)
    fields = ("title", "authors", "publisher", "publication_date")
    # filter_horizontal = ("authors", )
    filter_vertical = ("authors", )
    raw_id_fields = ("publisher", )

class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "website")


admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
