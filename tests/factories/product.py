import factory

from apps.products.models import ProductsModel


class ProductsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductsModel

    product_slug = factory.Faker("slug")
    url = "https://some_url.com/"
