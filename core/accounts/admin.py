from django.contrib import admin


# Register your models here.

from django.contrib.auth.admin import UserAdmin


from .models import CustomUser, Profile, Role


class CustomUserAdmin(UserAdmin):

    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "is_verified")
    list_filter = ("email", "is_staff", "is_active", "is_verified")
    fieldsets = (
        ("Autorization", {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                    "is_verified",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                    "is_verified",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin),
admin.site.register(Profile)
admin.site.register(Role)
