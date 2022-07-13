import pytest
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import UserModel


@pytest.mark.django_db
class TestUserModel:
    @classmethod
    def setup_class(cls):
        cls.model = UserModel

    def test_str(self, base_user):
        assert str(base_user) == base_user.name

    def test_parent_class(self):
        assert issubclass(self.model, AbstractUser)

    def test_email_field(self):
        field = self.model._meta.get_field("email")

        assert type(field) is models.EmailField
        assert field.max_length == 100
        assert field.unique is True
        assert field.verbose_name == _("User Email")

    def test_name_field(self):
        field = self.model._meta.get_field("name")

        assert type(field) is models.CharField
        assert field.max_length == 100
        assert field.verbose_name == _("User Name")

    def test_document_field(self):
        field = self.model._meta.get_field("document")

        assert type(field) is models.CharField
        assert field.max_length == 11
        assert field.verbose_name == _("User Document")
        assert field.help_text == _("Just numbers")

    def test_meta_verbose_name(self):
        assert self.model._meta.verbose_name == _("User")

    def test_meta_verbose_name_plural(self):
        assert self.model._meta.verbose_name_plural == _("Users")

    def test_len_fields(self):
        assert len(self.model._meta.fields) == 10
