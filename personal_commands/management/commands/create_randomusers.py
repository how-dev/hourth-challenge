from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker

from apps.user.models import UserModel
from services.cpf import CPFLogics


class Command(BaseCommand):
    def handle(self, *_, **options):
        fake = Faker()
        cpf = CPFLogics()

        for _ in range(100):
            fields = {
                "name": fake.first_name(),
                "email": fake.unique.email(),
                "password": make_password(fake.last_name()),
                "document": cpf.force_valid_cpf(),
                "is_staff": False,
                "is_superuser": False,
            }
            UserModel.objects.get_or_create(**fields)
        self.stdout.write(f"100 random users was created")
