from django.shortcuts import render
from .models import Post


def home(request):
    # third argument is optional and is the context which is a way for us to pass information into our template.
    # an http response is returned.
    # our views need to return an http response or an exception.
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


def about(request):
    return render(request, "blog/about.html", {"title": "About Page!!"})
