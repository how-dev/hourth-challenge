from unittest.mock import Mock, patch

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.utils.translation import gettext_lazy as _

from apps.user.admin import UserAdmin
from apps.user.models import UserModel


class TestUserAdmin:
    @classmethod
    def setup_class(cls):
        cls.admin = UserAdmin(UserModel, AdminSite())

    def test_meta_model(self):
        assert self.admin.model == UserModel

    def test_admin_subclass(self):
        assert issubclass(UserAdmin, admin.ModelAdmin)

    def test_readonly_fields(self):
        assert self.admin.readonly_fields == ["date_joined", "last_login"]

    def test_list_display(self):
        assert self.admin.list_display == [
            "__str__",
            "document",
            "is_superuser",
            "is_active",
            "last_login",
        ]

    def test_list_filter(self):
        assert self.admin.list_filter == ["is_superuser", "is_active", "last_login"]

    def test_search_fields(self):
        assert self.admin.search_fields == [
            "name",
            "document",
        ]

    def test_ordering(self):
        assert self.admin.ordering == ["id"]

    def test_list_per_page(self):
        assert self.admin.list_per_page == 15

    def test_fildset(self):
        assert self.admin.fieldsets == [
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

    def test_len_fieldsets(self):
        assert len(self.admin.fieldsets) == 3

    @patch("apps.user.admin.make_password")
    @patch("apps.user.admin.UserModel")
    def test_save_model_with_new_instance(self, mock_user_model, mock_make_password):
        obj = Mock()
        mock_user_model.objects.get.side_effect = ValueError()
        mock_user_model.DoesNotExist = ValueError

        self.admin.save_model(request=Mock(), obj=obj, form=Mock(), change=Mock())

        mock_user_model.objects.get.assert_called_once_with(id=obj.id)
        mock_make_password.assert_called_once()
        obj.save.assert_called_once()

    @patch("apps.user.admin.make_password")
    @patch("apps.user.admin.UserModel")
    def test_save_model_with_existent_instance(
        self, mock_user_model, mock_make_password
    ):
        obj = Mock()
        mock_user_model.objects.get.return_value = Mock()
        mock_user_model.DoesNotExist = ValueError

        self.admin.save_model(request=Mock(), obj=obj, form=Mock(), change=Mock())

        mock_user_model.objects.get.assert_called_once_with(id=obj.id)
        mock_make_password.assert_called_once()
        obj.save.assert_called_once()
