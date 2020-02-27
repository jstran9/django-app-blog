from django.urls import path
from . import views  # from the current directory just import the views module.

urlpatterns = [
    # if we want to do a reverse look-up and having a unique name can help us perform this look-up.
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
]
