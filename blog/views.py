from django.shortcuts import render


posts = [
    {
        "author": "CoreyMS",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "August 27, 2018",
    },
    {
        "author": "Jane Doe",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "August 28 2018",
    },
]


def home(request):
    # third argument is optional and is the context which is a way for us to pass information into our template.
    # an http response is returned.
    # our views need to return an http response or an exception.
    context = {"posts": posts}
    return render(request, "blog/home.html", context)


def about(request):
    return render(request, "blog/about.html", {"title": "About Page!!"})
