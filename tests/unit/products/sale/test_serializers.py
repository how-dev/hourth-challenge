from rest_framework import serializers

from apps.products.models import SalesModel
from apps.products.serializers import SalesSerializer


class TestSalesSerializer:
    @classmethod
    def setup_class(cls):
        cls.serializer = SalesSerializer

    def test_parent_class(self):
        assert issubclass(self.serializer, serializers.ModelSerializer)

    def test_meta_model(self):
        assert self.serializer.Meta.model is SalesModel

    def test_meta_fields(self):
        assert self.serializer.Meta.fields == ("id", "insertion_date")
