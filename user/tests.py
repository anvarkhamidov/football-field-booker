from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from user.models import User


class UserRegistrationTestCase(APITestCase):
    def post(self, url, payload):
        """
        Helper to send an HTTP post.

        @param (dict) payload: request body

        @returns: response
        """

        return self.client.post(url, payload, format="json")

    def test_user_registration(self):
        url = reverse("user-register")  # Replace with your URL
        data = {
            "phone_number": "8888888888",
            "password": "password123",
            "role": "user",
        }
        response = self.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.last().is_field_owner, False)

    def test_field_owner_registration(self):
        url = reverse("user-register")
        data = {
            "phone_number": "7777777777",
            "password": "password123",
            "role": "field_owner",
        }
        response = self.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.last().is_field_owner, True)

    def test_field_owner_can_see_own_fields(self):
        field_owner = User.objects.create_user(
            phone_number="5555555555", password="password", is_field_owner=True
        )
        field_owner_token = Token.objects.create(user=field_owner)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + field_owner_token.key
        )
        url = reverse("field-list")  # Replace with your URL
        response = self.client.get(url)
        # Field owner should only see their own fields
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 0
        )  # Assuming no fields are created for this owner yet
