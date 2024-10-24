from django.contrib.auth.models import Group
from django.db import migrations

from core.constants import UserRoles


def create_groups(apps, schema_editor):
    # Create groups for user role management
    Group.objects.get_or_create(name=UserRoles.FIELD_OWNER.value)
    Group.objects.get_or_create(name=UserRoles.USER.value)


def remove_groups(apps, schema_editor):
    # Delete groups for user role management
    Group.objects.filter(name=UserRoles.FIELD_OWNER.value).delete()
    Group.objects.filter(name=UserRoles.USER.value).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_groups, reverse_code=remove_groups),
    ]
