from django.db import models

from user.models import User


class Field(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    available_from = models.TimeField()
    available_to = models.TimeField()

    price_per_hour = models.DecimalField(max_digits=12, decimal_places=2)
    images = models.ImageField(
        upload_to="fields_images/", blank=True, null=True
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="fields"
    )

    def __str__(self):
        return self.name
