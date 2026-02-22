from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    # Keep it simple for the capstone: URL string instead of ImageField storage.
    profile_picture = models.URLField(blank=True)
    # Users this user follows
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )

    def __str__(self):
        return self.username
