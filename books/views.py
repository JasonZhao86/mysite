from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book
from .forms import ContactForm
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView
from .models import Publisher, Author
from django.shortcuts import get_object_or_404
from django.utils import timezone


def search_form(request):
    return render(request, "search_form.html")


def search(request):
    error = []
    if "q" in request.GET:
        if not request.GET["q"]:
            error.append("不允许为空")
        elif len(request.GET["q"]) > 20:
            error.append("长度必须小于等于20")
        else:
            q = request.GET["q"]
            result = Book.objects.filter(title__icontains=q)
            return render(request, "search_result.html", {"books": result, "search": q})
    return render(request, "search_form.html", {"error": error})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.is_valid())
            cd = form.cleaned_data
            subject = cd["subject"]
            message = cd["message"]
            email = cd.get("email", "nobody@163.com")
            # send_mail(subject, message, email, ["jason.zhao86@outlook.com"])
            return HttpResponseRedirect("/books/search/")
    else:
        form = ContactForm(initial={"subject": "I love your site"})
    return render(request, "contact-us.html", {"form": form})


class PublisherList(ListView):
    model = Publisher
    context_object_name = "publishers"


class PublisherDetail(DetailView):
    # model = Publisher
    queryset = Publisher.objects.all()

    def get_context_data(self, **kwargs):
        kwargs = super(PublisherDetail, self).get_context_data(**kwargs)
        kwargs.update({"books": Book.objects.all()})
        return kwargs


class BookList(ListView):
    queryset = Book.objects.all()
    # queryset = Book.objects.order_by("-publication_date")
    context_object_name = "book_list"
    template_name = "book_list.html"


class PublisherBooksList(ListView):
    template_name = "books/publisher-books.html"
    context_object_name = "book_list"

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.args[0])
        return Book.objects.filter(publisher=self.publisher)

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super(PublisherBooksList, self).get_context_data(**kwargs)
        content.update({"publisher": self.publisher})
        return content


class AuthorDetail(DetailView):
    model = Author

    def get_object(self, queryset=None):
        object = super(AuthorDetail, self).get_object(queryset)
        object.last_accessed = timezone.now()
        object.save()
        return object
