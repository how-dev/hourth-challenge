import pytest
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.products.models import ProductsModel, SalesModel
from services.base_model import BaseModel


@pytest.mark.django_db
class TestSalesModel:
    @classmethod
    def setup_class(cls):
        cls.model = SalesModel

    def test_str(self, base_sale):
        assert str(base_sale) == f"Sale of id {base_sale.id}"

    def test_parent_class(self):
        assert issubclass(self.model, BaseModel)

    def test_products_field(self):
        field = self.model._meta.get_field("products")

        assert type(field) is models.ForeignKey
        assert field.related_model is ProductsModel
        assert field.null is True
        assert field.blank is True
        assert field.verbose_name == _("Products")

    def test_insertion_date_field(self):
        field = self.model._meta.get_field("insertion_date")

        assert type(field) is models.DateField
        assert field.auto_now_add is True
        assert field.verbose_name == _("Insertion Date")

    def test_len_fields(self):
        assert len(self.model._meta.fields) == 5
