from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse


def index(request):
    return HttpResponse("Hello")


def register(request):
    if request.method == "POST":
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, "Account created successfully")
            return redirect(reverse("login"))

    else:
        f = UserCreationForm()

    return render(request, "social/register.html", {"form": f})
