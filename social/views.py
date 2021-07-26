from social.forms import PostForm
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Followers


@login_required
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


@login_required
def follow(request, pk):
    if request.method == "POST":
        if request.user.id == pk:
            return redirect(reverse("social:user_detail", kwargs={"pk": pk}))

        follower = request.user
        user = get_object_or_404(User, pk=pk)
        f = Followers.objects.create(user=user, follower=follower)
        f.save()
        return redirect(reverse("social:user_detail", kwargs={"pk": pk}))

    else:
        return redirect(reverse("social:user_detail", kwargs={"pk": pk}))


class UserDetailView(LoginRequiredMixin, DetailView, FormMixin):
    template_name = "social/user_detail.html"
    model = User
    form_class = PostForm

    def get_initial(self):
        obj = self.get_object()
        return {"author": obj.id}

    def get_success_url(self):
        return reverse("social:user_detail", kwargs={"pk": self.object.id})

    def post(self):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
