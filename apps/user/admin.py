from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        [_("Identification"), {"fields": ["name", "document"]}],
        [_("Credentials"), {"fields": ["email", "password"]}],
        [
            _("Administration"),
            {
                "fields": [
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "last_login",
                ]
            },
        ],
    ]
    readonly_fields = ["date_joined", "last_login"]
    list_display = ["__str__", "document", "is_superuser", "is_active", "last_login"]
    list_filter = ["is_superuser", "is_active", "last_login"]
    search_fields = [
        "name",
        "document",
    ]
    ordering = ["id"]
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        collaborator_id = obj.id
        try:
            collaborator = UserModel.objects.get(id=collaborator_id)
        except UserModel.DoesNotExist:
            obj.password = make_password(obj.password)
            obj.save()
        else:
            change_password = obj.password
            actual_password = collaborator.password

            if change_password != actual_password:
                obj.password = make_password(obj.password)

            obj.save()


admin.site.unregister(Group)
