from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=200, blank=True)
    website = models.URLField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


# Create your models here.
class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=50)
    platform = models.ForeignKey(StreamPlatform, related_name='watchlist', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0, null=True, blank=True)  # Average rating for the watchlist
    number_ratings = models.IntegerField(default=0, null=True, blank=True)  # Number of ratings received
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return str(self.title)
    
    
class Review(models.Model):
    review_user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(WatchList, related_name='reviews', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating)+" - " + str(self.watchlist.title) + " - " + str(self.review_user)