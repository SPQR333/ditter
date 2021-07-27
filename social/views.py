from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from social.forms import PostForm

from .models import Followers, Post


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "social/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["childrens"] = self.get_object().get_descendants()
        return context


def whoiam(request):
    return HttpResponse(request.user.username)


class IndexView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "social/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        following = [fol.user for fol in self.request.user.following.all()]
        res = Post.objects.filter(author__in=following).order_by("-pub_date")
        return list(res)


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
def unfollow(request, pk):
    if request.method == "POST":
        if request.user.id == pk:
            messages.error(request, "You can`t unfollow yourself")
            return redirect(reverse("social:user_detail", kwargs={"pk": pk}))

        follower = request.user
        user = get_object_or_404(User, pk=pk)
        if Followers.objects.filter(user=user, follower=follower).exists():
            Followers.objects.filter(user=user, follower=follower).delete()
        else:
            messages.error(request, "You can`t unfollow if you wasn`t followed")
        return redirect(reverse("social:user_detail", kwargs={"pk": pk}))

    else:
        return redirect(reverse("social:user_detail", kwargs={"pk": pk}))


@login_required
def follow(request, pk):
    if request.method == "POST":
        if request.user.id == pk:
            messages.error(request, "You can`t follow yourself")
            return redirect(reverse("social:user_detail", kwargs={"pk": pk}))

        follower = request.user
        user = get_object_or_404(User, pk=pk)
        if not Followers.objects.filter(user=user, follower=follower).exists():
            f = Followers.objects.create(user=user, follower=follower)
            f.save()
        else:
            messages.error(request, "You can`t follow twice")
        return redirect(reverse("social:user_detail", kwargs={"pk": pk}))

    else:
        return redirect(reverse("social:user_detail", kwargs={"pk": pk}))


class UserDetailView(LoginRequiredMixin, DetailView, FormMixin):
    template_name = "social/user_detail.html"
    model = User
    context_object_name = "u"
    form_class = PostForm

    def get_initial(self):
        obj = self.get_object()
        return {"author": obj.id}

    def get_success_url(self):
        return reverse("social:user_detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_following"] = Followers.objects.filter(
            user=self.get_object(), follower=self.request.user
        ).exists()
        return context

    def post(self):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
