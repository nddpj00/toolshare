from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=254)
    slug = models.SlugField(max_length=50)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField(null=True, blank = True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    


    def __str__(self):
        return self.title