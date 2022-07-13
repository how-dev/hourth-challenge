from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from apps.products.admin import ProductsAdmin, SalesInline
from apps.products.models import ProductsModel


class TestProductsAdmin:
    @classmethod
    def setup_class(cls):
        cls.admin = ProductsAdmin(ProductsModel, AdminSite())

    def test_meta_model(self):
        assert self.admin.model == ProductsModel

    def test_admin_subclass(self):
        assert issubclass(ProductsAdmin, admin.ModelAdmin)

    def test_list_display(self):
        assert self.admin.list_display == (
            "id",
            "url",
            "image",
            "insertion_date",
            "modification_date",
        )

    def test_readonly_fields(self):
        assert self.admin.readonly_fields == (
            "id",
            "insertion_date",
            "modification_date",
        )

    def test_inlines(self):
        assert self.admin.inlines == (SalesInline,)
