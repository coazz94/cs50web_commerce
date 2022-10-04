from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    image = models.ImageField()
    url = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
       return f"{self.name} costs {self.price}"

