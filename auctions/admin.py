from django.contrib import admin

# Register your models here.
from .models import *



admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Bid)