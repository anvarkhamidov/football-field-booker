from django.db import models

from field.models import Field
from user.models import User


class Booking(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.field.name} - {self.user.name}'
