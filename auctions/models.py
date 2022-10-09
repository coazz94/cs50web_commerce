from django.contrib.auth.models import AbstractUser
from django.db import models

from .forms import CATEGORIES

class User(AbstractUser):
    pass


class Listing(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    image = models.ImageField(null=True, blank=True, upload_to="auctions/static/test")
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    category = models.CharField(max_length=15, default="not_defined", choices=CATEGORIES)
    active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created")
    

    def __str__(self):
       return f"{self.title} costs {self.price}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, blank=True,  on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.user.username} listed {self.listing.title}"



class Bid(models.Model):
    """Bid model contains all info about single bid:
    * price
    * who bid
    * when
    * on what auction
    """

    # Model fields
    # auto: bid_id
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2)

    class Meta:
        verbose_name = "bid"
        verbose_name_plural = "bids"

    def __str__(self):
        return f"{self.user} bid {self.bid_price}  on {self.listing.title}"

"""
class Company(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

    
class Language(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Programmer(models.Model):
    name = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    language = models.ManyToManyField(Language)

    def __str__(self):
        return self.name

"""