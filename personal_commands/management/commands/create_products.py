import random

from django.core.management.base import BaseCommand
from faker import Faker

from apps.products.models import ProductsModel, SalesModel


class Command(BaseCommand):
    def handle(self, *_, **options):
        fake = Faker()

        for _ in range(100):
            product = ProductsModel.objects.create(
                product_slug=fake.unique.slug(), url=fake.unique.url()
            )
            for _ in range(random.randrange(1, 6)):
                SalesModel.objects.create(products=product)

        self.stdout.write(f"100 products was created")
