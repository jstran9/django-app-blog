"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # if we go to the path of "blog" we be mapping to our urls.py module.
    # for example: if we go to "blog/" then we will currently be mapping to the home function in our views from the blog app.
    # note that if do something like "blog/home" then when we forward this request into the "urls.py" file from the blogs app then we will be looking for a path to match "/home" because we have already matched the "blog" portion.
    # by default even if we don't have a trailing forward slash then Django will re-direct routes without a trailing forward slash to the ones with a trailing forward slash.
    # path('blog/', include('blog.urls')), # make the blog require a different route.
    path('', include('blog.urls')),  # make our blog application our home page.
]
