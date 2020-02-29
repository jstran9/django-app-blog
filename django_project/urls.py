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
from django.contrib.auth import (
    views as auth_views,
)  # multiple views so we need to avoid naming collisions.
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # if we go to the path of "blog" we be mapping to our urls.py module.
    # for example: if we go to "blog/" then we will currently be mapping to the home function in our views from the blog app.
    # note that if do something like "blog/home" then when we forward this request into the "urls.py" file from the blogs app then we will be looking for a path to match "/home" because we have already matched the "blog" portion.
    # by default even if we don't have a trailing forward slash then Django will re-direct routes without a trailing forward slash to the ones with a trailing forward slash.
    # path('blog/', include('blog.urls')), # make the blog require a different route.
    path("", include("blog.urls")),  # make our blog application our home page.
    path("register/", user_views.register, name="register"),
    path("profile/", user_views.profile, name="profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if we are currently in debug mode then we will add the static statement.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
