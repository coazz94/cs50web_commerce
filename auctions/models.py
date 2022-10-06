from django.contrib.auth.models import AbstractUser
from django.db import models

from .forms import CATEGORIES

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Listing(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    category = models.CharField(max_length=15, default="not_defined", choices=CATEGORIES)

    def __str__(self):
       return f"{self.title} costs {self.price}"



class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    items = models.ManyToManyField(Listing, blank=True, related_name="listing")


    def __str__(self):
        return f"{self.user}"



"""

    Welcher User hat das Listing ertsellt Wie
    Bieten auf den Artikel ( price tag bei model from listing ka wie)

"""