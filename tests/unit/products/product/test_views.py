from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.products.filters import ProductsFilter
from apps.products.serializers import ProductsSerializer
from apps.products.views import ProductsViewSet
from apps.user.permissions import UserPermissions


class TestProductsViewSet:
    @classmethod
    def setup_class(cls):
        cls.view = ProductsViewSet

    def test_parent_class(self):
        assert issubclass(ProductsViewSet, ReadOnlyModelViewSet)

    def test_serializer_class_attr(self):
        assert self.view.serializer_class == ProductsSerializer

    def test_authentication_classes_attr(self):
        assert self.view.authentication_classes == [TokenAuthentication]

    def test_permission_classes_attr(self):
        assert self.view.permission_classes == [UserPermissions]

    def test_throttle_classes_attr(self):
        assert self.view.throttle_classes == [UserRateThrottle]

    def test_filter_backends_attr(self):
        assert self.view.filter_backends == [DjangoFilterBackend]

    def test_filterset_class_attr(self):
        assert self.view.filterset_class == ProductsFilter
