from rest_framework import serializers

from apps.user.models import UserModel
from apps.user.serializers import LoginSerializer, UserSerializer


class TestLoginSerializer:
    @classmethod
    def setup_class(cls):
        cls.serializer = LoginSerializer

    def test_parent_class(self):
        assert issubclass(LoginSerializer, serializers.Serializer)

    def test_email_field(self):
        field = self.serializer._declared_fields.get("email")

        assert type(field) == serializers.CharField

    def test_password_field(self):
        field = self.serializer._declared_fields.get("password")

        assert type(field) == serializers.CharField


class TestUserSerializer:
    @classmethod
    def setup_class(cls):
        cls.serializer = UserSerializer

    def test_parent_class(self):
        assert issubclass(self.serializer, serializers.ModelSerializer)

    def test_meta_model(self):
        assert self.serializer.Meta.model is UserModel

    def test_meta_fields(self):
        assert self.serializer.Meta.fields == "__all__"

    def test_meta_extra_kwargs(self):
        assert self.serializer.Meta.extra_kwargs == {
            "password": {"write_only": True},
            "is_active": {"write_only": True},
            "date_joined": {"write_only": True},
        }
