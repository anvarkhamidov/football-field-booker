from django.db import models

from field.models import Field
from user.models import User


class Booking(models.Model):
    field = models.ForeignKey(
        Field, on_delete=models.CASCADE, related_name="bookings"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings"
    )
    date = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    total_cost = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.field.name} - {self.user.phone_number} on {self.date}"
