from django.db import models
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        related_name='profile', 
        on_delete=models.CASCADE
    )
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    links = models.URLField(max_length=200, null=True, blank=True) 

    def __str__(self):
        return f"{self.user.username}'s Profile"
