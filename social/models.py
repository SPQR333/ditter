from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import timezone


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, blank=False, null=False)
    content = models.TextField(max_length=1024, blank=False, null=False)
    pub_date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"<{self.title} by {self.author.username}>"

    class Meta:
        unique_together = [("author", "title")]


class Followers(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        blank=False,
        null=False,
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        blank=False,
        null=False,
    )

    def __str__(self):
        return f"<{self.follower.username} following {self.user.username}>"

    class Meta:
        unique_together = [("user", "follower")]
