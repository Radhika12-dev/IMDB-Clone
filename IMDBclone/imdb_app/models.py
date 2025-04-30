from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class StreamingPlatform(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField()
    website = models.URLField(max_length=255)
    
    def __str__(self):
        return self.name

class WatchList(models.Model):
    title = models.CharField(max_length=255)
    storyline = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey(StreamingPlatform, related_name='watchlist', on_delete=models.CASCADE, null=True, blank=True)
    avg_rating = models.FloatField(default=0.0)
    total_ratings = models.IntegerField(default=0)
    def __str__(self):
        return self.title


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    #One movie can have multiple reviews, but one review belongs to one movie
    watchlist = models.ForeignKey(WatchList, related_name='reviews', on_delete=models.CASCADE)

    def __str__(self):
        return self.watchlist.title + " - " + str(self.rating)