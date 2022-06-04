from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    prouser = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to = 'images/',
        blank = True,
        null = True,
    )

    def __str__(self):
        return self.prouser.username