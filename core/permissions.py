from rest_framework import permissions

from core.constants import UserRoles


class IsFieldOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if user is field_owner
        return request.user.groups.filter(
            name=UserRoles.FIELD_OWNER.value
        ).exists()
