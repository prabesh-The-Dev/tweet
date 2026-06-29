from django.db import models
from django.contrib.auth.models import User


class tweet(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tittle = models.TextField(max_length=50)
    desc = models.TextField()
    imag = models.ImageField(upload_to='details/', null=True, blank=True)

    def __str__(self):
        return self.tittle
