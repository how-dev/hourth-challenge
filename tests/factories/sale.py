import factory

from apps.products.models import SalesModel
from tests.factories.product import ProductsFactory


class SalesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SalesModel

    products = factory.SubFactory(ProductsFactory)
