from unittest.mock import patch

import pytest
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.products.models import ProductsModel
from apps.products.serializers import ProductsSerializer


class TestProductsSerializer:
    @classmethod
    def setup_class(cls):
        cls.serializer = ProductsSerializer

    def test_parent_class(self):
        assert issubclass(self.serializer, serializers.ModelSerializer)

    def test_meta_model(self):
        assert self.serializer.Meta.model is ProductsModel

    def test_meta_fields(self):
        assert self.serializer.Meta.fields == (
            "id",
            "image",
            "url",
            "insertion_date",
            "sales",
        )

    @patch("apps.products.serializers.datetime")
    def test_validate_date_format(self, mock_datetime):
        mock_datetime.strptime.side_effect = ValueError()

        with pytest.raises(ValidationError) as err:
            self.serializer.validate_date_format("202-02-000")

        assert err.value.detail == {
            "detail": "Incorrect data format, should be YYYY-MM-DD"
        }
