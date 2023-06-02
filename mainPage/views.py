from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User
# Create your views here.

def mainPage(request):
    return render(request, "mainPage/mainPage.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("mainPage"))
        else:
            return render(request, "mainPage/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mainPage/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("mainPage"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mainPage/register.html", {
                "message": "Passwords didn't match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username = username, password = password)
            user.save()
        except IntegrityError:
            return render(request, "mainPage/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("mainPage"))
    else:
        return render(request, "mainPage/register.html")