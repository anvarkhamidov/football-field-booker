from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.constants import UserRoles
from .models import User  # Ваша модель пользователя


@receiver(post_save, sender=User)
def add_to_default_group(sender, instance, created, **kwargs):
    if instance.is_superuser:
        return

    if instance.is_field_owner:  # If user is field owner
        if not Group.objects.filter(name=UserRoles.FIELD_OWNER.value).exists():
            owner_group = Group.objects.get(name=UserRoles.FIELD_OWNER.value)
            instance.groups.add(owner_group)
    else:
        if not Group.objects.filter(name=UserRoles.USER.value).exists():
            user_group = Group.objects.get(name=UserRoles.USER.value)
            instance.groups.add(user_group)
