from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


def home(request):
    # third argument is optional and is the context which is a way for us to pass information into our template.
    # an http response is returned.
    # our views need to return an http response or an exception.
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    # set a new template.
    template_name = "blog/home.html"  # <app>/<model>_<viewtype>.html
    # set the context's objects.
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    # set a new template.
    template_name = "blog/user_posts.html"  # <app>/<model>_<viewtype>.html
    # set the context's objects.
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        # kwargs: gives us access to query parameters
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        # before the form is submitted take the instance of the form and set its author to the logged in author.
        form.instance.author = self.request.user
        # run the parent form_valid after setting the author.
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        # before the form is submitted take the instance of the form and set its author to the logged in author.
        form.instance.author = self.request.user
        # run the parent form_valid after setting the author.
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", {"title": "About Page!!"})
