from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from core.constants import UserRoles
from field.models import Field
from user.models import User


class FieldTestCase(APITestCase):
    def post(self, url, payload):
        """
        Helper to send an HTTP post.

        @param (dict) payload: request body

        @returns: response
        """

        return self.client.post(url, payload, format="json")

    def setUp(self):
        self.owner = User.objects.create_user(
            phone_number="9999999999", password="password", is_field_owner=True
        )
        self.user = User.objects.create_user(
            phone_number="8888888888", password="password"
        )
        Group.objects.get(name=UserRoles.FIELD_OWNER.value).user_set.add(
            self.owner
        )
        Group.objects.get(name=UserRoles.USER.value).user_set.add(self.user)
        self.field1 = Field.objects.create(
            name="Field 1",
            address="Location 1",
            contact_info="field1@test.com",
            description="Test Field 1",
            longitude=40.0,
            latitude=50.0,
            available_from="10:00",
            available_to="18:00",
            price_per_hour=100,
            owner=self.owner,
        )
        self.field2 = Field.objects.create(
            name="Field 2",
            address="Location 2",
            contact_info="field2@test.com",
            description="Test Field 2",
            longitude=41.0,
            latitude=51.0,
            available_from="10:00",
            available_to="18:00",
            price_per_hour=200,
            owner=self.owner,
        )
        self.token_user, _ = Token.objects.get_or_create(user=self.user)
        self.token_owner, _ = Token.objects.get_or_create(user=self.owner)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_user.key
        )

    def test_list_fields_sorted_by_distance(self):
        url = reverse("field-list")
        # >>> calculate_distance(50.5,40.5,50.0,40.0)
        # 65.99179674080648 (Field 1)
        # >>> calculate_distance(50.5,40.5,51.0,41.0)
        # 65.79086659654897 (Field 2)
        response = self.client.get(url, {"latitude": 50.5, "longitude": 40.5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = response.data
        self.assertEqual(len(fields), 2)
        # Ensure fields are ordered by distance
        self.assertEqual(fields[0]["name"], "Field 2")

    def test_field_creation(self):
        url = reverse("field-list")  # Replace with your URL
        data = {
            "name": "New Field",
            "address": "New Address",
            "contact_info": "new@test.com",
            "description": "A new field",
            "longitude": 40.0,
            "latitude": 50.0,
            "available_from": "10:00",
            "available_to": "18:00",
            "price_per_hour": 150,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_owner.key
        )
        response = self.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.last().owner, self.owner)
