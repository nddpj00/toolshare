from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    organiser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=254)
    slug = models.SlugField(max_length=50)
    body = models.TextField()
    date = models.DateTimeField()
    attendees = models.ManyToManyField(User, related_name='events_attending', blank=True)
    interested = models.ManyToManyField(User, related_name='events_interested', blank=True)
    location = models.CharField(max_length=254, null=True, blank=True)
    thumb = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title
