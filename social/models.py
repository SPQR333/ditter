from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = models.TextField(max_length=1024)

    def __repr__(self) -> str:
        return f"<{self.title}>"
