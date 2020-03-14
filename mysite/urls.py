"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .views import (
    hello, curtime, curtimes, get_request_meta,
    view_1, view_2, cookie_and_session_demo,
    login, logout
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^hello/$', hello),
    url(r'^curtime/$', curtime),
    url(r'^curtimes/(\d{1,2})/$', curtimes, name="mysite-curtime"),
    url(r'^get_meta/$', get_request_meta),
    url(r'^view1/$', view_1),
    url(r'^view2/$', view_2),
    url(r'^cookie_and_session_demo/$', cookie_and_session_demo),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^books/', include("books.urls")),
]
