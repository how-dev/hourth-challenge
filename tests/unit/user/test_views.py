from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet, ViewSet

from apps.user.filters import UserFilter
from apps.user.permissions import UserPermissions
from apps.user.serializers import UserSerializer
from apps.user.views import UserLoginViewSet, UserViewSet


class TestUserViewSet:
    @classmethod
    def setup_class(cls):
        cls.view = UserViewSet

    def test_parent_class(self):
        assert issubclass(UserViewSet, ModelViewSet)

    def test_serializer_class_attr(self):
        assert self.view.serializer_class == UserSerializer

    def test_authentication_classes_attr(self):
        assert self.view.authentication_classes == [TokenAuthentication]

    def test_permission_classes_attr(self):
        assert self.view.permission_classes == [UserPermissions]

    def test_throttle_classes_attr(self):
        assert self.view.throttle_classes == [UserRateThrottle]

    def test_filter_backends_attr(self):
        assert self.view.filter_backends == [DjangoFilterBackend]

    def test_filterset_class_attr(self):
        assert self.view.filterset_class == UserFilter


class TestUserLoginViewSet:
    @classmethod
    def setup_class(cls):
        cls.view = UserLoginViewSet

    def test_parent_class(self):
        assert issubclass(self.view, ViewSet)
