from django.db import models

from user.models import User


class Field(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    images = models.ImageField(upload_to='fields/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fields')

    def __str__(self):
        return self.name
