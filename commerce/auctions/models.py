from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import AutoField, CharField, DateTimeField, FloatField, BooleanField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.files import FileField


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    pass

class AuctionListing(models.Model):
    listing_id = AutoField(primary_key=True)
    seller = ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    item_name = CharField(max_length=150, null=False)
    item_description = CharField(max_length=300)
    img = FileField(upload_to="auctions/static/auctions/imgs")
    category = CharField(max_length=25)
    current_price = FloatField()
    sell_date = DateTimeField()
    is_active = BooleanField()

    def __str__(self):
        return f"{self.listing_id}: {self.item_name} ({self.item_description}) put up by {self.seller} on {self.sell_date} for ${self.current_price}"

class Bid(models.Model):
    bid_id = AutoField(primary_key=True)
    bidding_on = ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing")
    bid_amt = FloatField()
    bid_by = ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")

    def __str__(self):
        return f"{self.bid_id}: ${self.bid_amt} on ({self.bidding_on}) by ({self.bid_by}) "

class Comment(models.Model):
    comment_id = AutoField(primary_key=True)
    comment_txt = CharField(max_length=2048)
    commenter = ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")
    commented_on = ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="commented_on")
    commented_when = DateTimeField()

    def __str__(self):
        return f"{self.comment_id}: {self.comment_txt} posted by {self.commenter} on {self.commented_on}, {self.commented_when}"

class Watchlist(models.Model):
    watcher = ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    watched = ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watched")
    still_watching = BooleanField()

    def __str__(self):
        return f"{self.watcher} is watching {self.watched.item_name}"