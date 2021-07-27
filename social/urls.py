from django.urls import path
from . import views

app_name = "social"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("register/", views.register, name="register"),
    path("user/<int:pk>", views.UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/follow", views.follow, name="follow"),
    path("user/<int:pk>/unfollow", views.unfollow, name="unfollow"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name="post_detail"),
    path("whoiam/", views.whoiam),
]
