from django.urls import path

from booking.views import (
    BookingDeleteView,
    BookingListCreateView,
)

urlpatterns = [
    path(
        "bookings", BookingListCreateView.as_view(), name="booking-list-create"
    ),
    path(
        "bookings/<int:pk>", BookingDeleteView.as_view(), name="booking-delete"
    ),
]
