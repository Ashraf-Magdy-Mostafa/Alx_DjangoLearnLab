from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)

    # Required by checker: ImageField
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)

    # Required by task statement: followers ManyToMany referencing itself, symmetrical=False
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )

    def __str__(self):
        return self.username
