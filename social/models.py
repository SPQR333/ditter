from django.db import models
from django.contrib.auth.models import User
from django.urls.base import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(
        upload_to="avatars/",
    )

    def __str__(self):
        return f"<{self.user.username}`s avatar>"


class Post(MPTTModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1024, blank=False, null=False)
    pub_date = models.DateField(auto_now=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def get_absolute_url(self):
        return reverse("social:post_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"<{self.text} by {self.author.username}>"

    class MPTTMeta:
        order_insertion_by = ["pub_date"]


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
