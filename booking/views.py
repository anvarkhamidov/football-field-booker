from datetime import datetime

from rest_framework import generics, serializers
from rest_framework import permissions

from booking.models import Booking
from booking.serializers import (
    BookingListSerializer,
    BookingCreateSerializer,
    BookingDeleteSerializer,
)
from core.permissions import IsFieldOwner
from field.models import Field


class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookingListSerializer
        return BookingCreateSerializer

    def perform_create(self, serializer):
        dt1 = datetime.combine(
            datetime.now(), serializer.validated_data["time_to"]
        )
        dt2 = datetime.combine(
            datetime.now(), serializer.validated_data["time_from"]
        )

        if field := Field.objects.filter(
            id=serializer.validated_data["field_id"]
        ).first():
            total_cost = (
                float(field.price_per_hour)
                * (dt1 - dt2).total_seconds()
                // 3600
            )
            # Automatically associate the booking with the logged-in user
            serializer.save(
                user=self.request.user,
                total_cost=total_cost,
                field=field,
            )
        else:
            raise serializers.ValidationError("Field does not exist.")

    def get_permissions(self):
        # Apply IsFieldOwner permission for the 'GET' method
        if self.request.method == "GET":
            if self.request.user.is_superuser:
                return [permissions.IsAdminUser()]
            return [permissions.IsAuthenticated(), IsFieldOwner()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Show only the bookings of the logged-in user
        if (
            self.request.user.is_authenticated
        ):  # Swagger tries to inspect and because of permission, getting AnonymusUser
            if self.request.user.is_superuser:
                return Booking.objects.all().prefetch_related("field", "user")
            return Booking.objects.filter(
                field__owner=self.request.user
            ).prefetch_related("field", "user")


class BookingDeleteView(generics.DestroyAPIView):
    serializer_class = BookingDeleteSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        IsFieldOwner,
    ]

    def get_queryset(self):
        if (
            self.request.user.is_authenticated
        ):  # Swagger tries to inspect and because of permission, getting AnonymusUser
            return Booking.objects.filter(field__owner=self.request.user)
