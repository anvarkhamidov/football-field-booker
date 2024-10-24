from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from core.constants import UserRoles
from user.models import User

UserRoleChoices = [
    ("user", UserRoles.USER.value),
    ("field_owner", UserRoles.FIELD_OWNER.value),
]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "is_field_owner",
            "first_name",
            "last_name",
        ]


class UserRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.ChoiceField(choices=UserRoleChoices)

    class Meta:
        model = User
        fields = ["phone_number", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.pop("role")
        user = User(**validated_data)
        if role == "field_owner":
            user.is_field_owner = True
        user.set_password(validated_data["password"])  # Hash the password
        try:
            user.save()
            Token.objects.create(user=user)  # Token authentication

            role_real_value = dict(UserRoleChoices)[role]
            group = Group.objects.get(
                name=UserRoles(role_real_value).value
            )  # Add to corresponding group
            user.groups.add(group)

            return user
        except Exception as e:
            print(e)
            user.delete()
            raise serializers.ValidationError("Failed to register")
