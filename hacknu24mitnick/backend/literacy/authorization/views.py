from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth import login as base_login, logout as base_logout
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic.edit import CreateView

from authorization.forms import UserLoginForm, UserRegisterForm
from authorization.models import User


# Create your views here.


class UserLoginView(LoginView):
    template_name = "authorization/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy("courses:base_page")


def logout(request):
    if request.user.is_authenticated:
        base_logout(request)
    return HttpResponseRedirect(reverse_lazy("courses:base_page"))


def register(request):
    if request.method == "GET":
        form = UserRegisterForm()
        context = {"form": form}
        return render(request, context=context, template_name="authorization/register.html")
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
        )
        if user:
            base_login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect(reverse("courses:base_page"))
    context = {"form": form}
    return render(request, context=context, template_name="authorization/register.html")
