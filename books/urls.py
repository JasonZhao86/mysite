from django.conf.urls import url
from .views import (
    search_form, search, contact,
    PublisherList, PublisherDetail, BookList, PublisherBooksList, AuthorDetail,
)

urlpatterns = [
    url(r'^search-form/$', search_form),
    url(r'^search/$', search),
    url(r'^contact/$', contact),
    url(r'^publishers/$', PublisherList.as_view()),
    url(r'^publisher/(?P<pk>\d+)/$', PublisherDetail.as_view()),
    url(r'^publisher-books/([\w-]+)/$', PublisherBooksList.as_view()),
    url(r'^books/$', BookList.as_view()),
    url(r'^author/(?P<pk>\d+)/$', AuthorDetail.as_view()),
]