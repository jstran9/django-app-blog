from django.shortcuts import render, redirect
from django.contrib import messages  # flash message to show we received valid data.
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == "POST":
        # instantiate form with the post data.
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # cleaned data gets nicely formatted data in Python objects.
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Your account has been created! You are now able to log in!"
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)
    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)

