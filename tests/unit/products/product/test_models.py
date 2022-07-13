import freezegun
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.products.models import ProductsModel
from services.base_model import BaseModel


@pytest.mark.django_db
class TestProductsModel:
    @classmethod
    def setup_class(cls):
        cls.model = ProductsModel

    def test_str(self, base_product):
        assert str(base_product) == f"Product of id {base_product.id}"

    def test_parent_class(self):
        assert issubclass(self.model, BaseModel)

    def test_image_field(self):
        field = self.model._meta.get_field("image")

        assert type(field) is models.FileField
        assert field.upload_to.__name__ == "product_directory_path"
        assert field.null is True
        assert field.blank is True
        assert field.verbose_name == _("Product Image")

    def test_product_slug_field(self):
        field = self.model._meta.get_field("product_slug")

        assert type(field) is models.SlugField
        assert field.unique is True
        assert field.verbose_name == _("Product Slug")

    def test_url_field(self):
        field = self.model._meta.get_field("url")

        assert type(field) is models.URLField
        assert field.verbose_name == _("Product Url")

    def test_meta_verbose_name(self):
        assert self.model._meta.verbose_name == "Product"

    def test_meta_verbose_name_plural(self):
        assert self.model._meta.verbose_name_plural == "Products"

    @freezegun.freeze_time("2022-1-1")
    def test_image_path_property(self, base_product):
        file = SimpleUploadedFile("requirements.txt", b"/requirements.txt")
        base_product.image = file
        base_product.save()

        assert (
            base_product.image_path
            == f"media/{base_product.product_slug}_01012022_000000_requirements.txt"
        )

    def test_len_fields(self):
        assert len(self.model._meta.fields) == 7
