from email.policy import default
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models

from .forms import CATEGORIES

class User(AbstractUser):
    pass


class Listing(models.Model):
    """Listing contains all info about the item:
    * id
    * title of the item
    * description of the item 
    * price of the item
    * category of the item
    * active status of the item
    * created by item
    * winner of item
    """

    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    #image = models.ImageField(null=True, blank=True, upload_to="images/")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    category = models.CharField(max_length=15, default="not_defined", choices=CATEGORIES)
    active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created")
    winner = models.ForeignKey( User, null = True, blank=True, on_delete=models.CASCADE, related_name="winner")
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
       return f"{self.title} costs {self.price}"

    # Implement if you want to use Image upload
    #@property  
    #def image_url(self):
    #    if self.image and hasattr(self.image, 'url'):
    #        return self.image.url
    #    else:
    #        return "https://wichtech.com/wp-content/uploads/2016/09/noimg.jpg"

    @property
    def image_link(self):
        if self.image_url:
            return self.image_url
        else:
            return "https://wichtech.com/wp-content/uploads/2016/09/noimg.jpg"    

class Watchlist(models.Model):
    """Watchlist model contains all info about the watchlist:
    * user
    * what items
    """
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

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2)


    def __str__(self):
        return f"{self.user} bid {self.bid_price}  on {self.listing.title}"


class Comments(models.Model):
    """Comments model contains all info about the comments:
    * what listing
    * what user made it
    * when
    * text of it
    """

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=500)


    def __str__(self):
        return f"{self.user} has made this comment {self.comment}"