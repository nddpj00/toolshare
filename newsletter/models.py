from django.db import models
from django.contrib.auth.models import User

class Newsletter(models.Model):
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_registered_already = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email