from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from apps.products.admin import SalesAdmin
from apps.products.models import SalesModel


class TestSalesAdmin:
    @classmethod
    def setup_class(cls):
        cls.admin = SalesAdmin(SalesModel, AdminSite())

    def test_meta_model(self):
        assert self.admin.model == SalesModel

    def test_admin_subclass(self):
        assert issubclass(SalesAdmin, admin.ModelAdmin)

    def test_list_display(self):
        assert self.admin.list_display == ("id", "insertion_date", "modification_date")
