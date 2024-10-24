from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone_number",
        "first_name",
        "last_name",
        "is_superuser",
    )
