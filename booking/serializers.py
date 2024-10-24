from rest_framework import serializers

from booking.models import Booking
from field.serializers import FieldSerializer
from user.serializers import UserSerializer


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    field = FieldSerializer(read_only=True)
    total_cost = serializers.FloatField(read_only=True)
    field_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "field",
            "field_id",
            "user",
            "date",
            "time_from",
            "time_to",
            "created_at",
            "total_cost",
        ]

    def validate(self, data):
        # Add custom validation to check if the field is available during the requested time
        if Booking.objects.filter(
            field_id=data["field_id"],
            time_from__lt=data["time_to"],
            time_to__gt=data["time_from"],
        ).exists():
            raise serializers.ValidationError(
                "Field is already booked for this time."
            )
        return data
