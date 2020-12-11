from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import Category


# Create your models here.

class User(AbstractUser):
    display_picture = models.ImageField(blank=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True)
    # following = models.ManyToManyField(Category,related_name="followed_by")

    def __str__(self):
        return self.username
