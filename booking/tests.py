from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from core.constants import UserRoles
from .models import Booking, Field, User


class BookingTestCase(APITestCase):
    def post(self, url, payload):
        """
        Helper to send an HTTP post.

        @param (dict) payload: request body

        @returns: response
        """

        return self.client.post(url, payload, format="json")

    def setUp(self):
        self.owner = User.objects.create_user(
            phone_number="9999999999",
            password="password",
            is_field_owner=True,
        )
        self.user = User.objects.create_user(
            phone_number="8888888888",
            password="password",
        )
        Group.objects.get(name=UserRoles.FIELD_OWNER.value).user_set.add(
            self.owner
        )
        Group.objects.get(name=UserRoles.USER.value).user_set.add(self.user)
        self.field = Field.objects.create(
            name="Test Field",
            address="123 Test St",
            contact_info="test@test.com",
            description="A test field",
            longitude=40.0,
            latitude=50.0,
            available_from="10:00",
            available_to="18:00",
            price_per_hour=100,
            owner=self.owner,
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_successful_booking_creation(self):
        url = reverse("booking-list-create")  # Replace with your URL
        data = {
            "field_id": self.field.id,
            "date": timezone.now().date(),
            "time_from": "11:00",
            "time_to": "12:00",
        }
        response = self.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().total_cost, 100)

    def test_booking_overlap(self):
        # Create an initial booking
        Booking.objects.create(
            user=self.user,
            field=self.field,
            date=timezone.now().date(),
            time_from="11:00",
            time_to="12:00",
            total_cost=100,
        )
        url = reverse("booking-list-create")
        data = {
            "field_id": self.field.id,
            "date": timezone.now().date(),
            "time_from": "11:30",  # Overlaps with previous booking
            "time_to": "12:30",
        }
        response = self.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Field is already booked", response.data["non_field_errors"][0]
        )
