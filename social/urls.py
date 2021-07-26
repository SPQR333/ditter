from django.urls import path
from . import views

app_name = "social"
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("user/<int:pk>", views.UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/follow", views.follow, name="follow"),
]
