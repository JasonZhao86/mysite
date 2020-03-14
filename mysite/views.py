from django.http import HttpResponse, Http404
import datetime
from django import template
from django.template import Context, Template, loader, RequestContext
from django.shortcuts import render, render_to_response
from .context_processors import custom_proc
from django.contrib import auth
from books.models import Author


def hello(request):
    class Person(object):
        def __init__(self, first_name, age):
            self.first_name, self.age = first_name, age

    class SlientVariableFailure(Exception):
        # pass
        silent_variable_failure = True

    class PersonClass3(object):
        def first_name(self):
            raise SlientVariableFailure()

    class Account(object):
        def delete(self):
            return "gai"
    t = template.Template("my name is {{ person.delete }}")
    # c = template.Context({"person": "zhaoxuan"})
    # c = template.Context({"person": "18"})
    # c = template.Context({"person": datetime.date(2020, 2, 19)})
    c = template.Context({"person": Account()})
    # print(t.render(c))
    print(request.path)
    print(request.get_full_path())
    print(request.is_secure())
    print(request.get_host())
    print(request.META["HTTP_USER_AGENT"])
    print(request.META["REMOTE_ADDR"])
    # print(request.META["HTTP_REFERER"])
    return HttpResponse("Hello World")


def curtime(request):
    nowtime = datetime.datetime.now()
    nowtime_str = datetime.datetime.strftime(nowtime, "%Y-%m-%d %H:%M:%S")
    # t = get_template("current_time.html")
    # return HttpResponse(t.render({"curtime": nowtime_str}))
    # return render(request, "current_time.html", {"curtime": nowtime_str, "person": {"name": "zhaoxuan", "age": 18}})
    return render(request, "curtime.html", {"curtime": nowtime_str})


def curtimes(request, offset):
    try:
        offset_i = int(offset)
    except ValueError:
        return Http404()
    nowtime = datetime.datetime.now()
    nowtime_str = datetime.datetime.strftime(
        nowtime + datetime.timedelta(hours=offset_i),
        "%Y-%m-%d %H:%M:%S"
    )
    # assert False
    # return HttpResponse(nowtime_str)
    return render(request, "futuretime.html", {"futuretime": nowtime_str})


def get_request_meta(request):
    values = request.META.items()
    list(values).sort()
    return render(request, "request_meta_info.html", {"re": values})


def view_1(request):
    t = loader.get_template("view1_t.html")
    # c = {
    #     'app': 'My app',
    #     'user': request.user,
    #     'ip_address': request.META['REMOTE_ADDR'],
    #     'message': 'I am view 1.'
    # }
    c = custom_proc(request)
    c.update({'message': 'I am view 1.'})
    return render(request, "view1_t.html", c)



def view_2(request):
    author = Author.objects.get(id=1)
    t = loader.get_template("view2_t.html")
    # c = {
    #     'app': 'My app',
    #     'user': request.user,
    #     'ip_address': request.META['REMOTE_ADDR'],
    #     'message': 'I am view 2.'
    # }
    c = custom_proc(request)
    c.update({
        'message': 'I am view 2.',
        'data': '<b>粗体</b>',
        "author": author,
        "datetime": datetime.datetime.now()
    })
    # return HttpResponse(t.render(c))
    return render(request, "view2_t.html", c)


def cookie_and_session_demo(request):
    """
    if "sessionid" in request.COOKIES:
        return HttpResponse("Your sessionid is %s" % request.COOKIES["sessionid"])
    return HttpResponse("Thanks, no sessionid in your cookie.")
    """

    """
    if "favorite_color" in request.GET:
        response = HttpResponse("Your favorite color is now %s" % request.GET["favorite_color"])
        response.set_cookie("favorite_color", request.GET["favorite_color"])
        return response
    return HttpResponse("You didn't give a favorite color.")
    """
    request.session["fav_color"] = "blue"
    print(request.session["fav_color"])
    return HttpResponse(request.session["fav_color"])


def login(request):
    """
    if request.user.is_authenticated:
        return HttpResponse("已认证用户，用户名为%s" % request.user.username)
    return  HttpResponse("未认证用户")
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponse("登陆成功")
        return HttpResponse("用户名或密码错误")
    return render_to_response("login.html")


def logout(request):
    auth.logout(request)
    return HttpResponse("注销成功")
