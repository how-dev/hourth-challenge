from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from apps.user.models import UserModel
from services.cpf import CPFLogics


class Command(BaseCommand):
    def handle(self, *_, **options):
        cpf = CPFLogics()
        email = "base@tester.com"
        password = make_password("base")

        fields = {
            "name": "Base Superuser",
            "email": email,
            "password": password,
            "document": cpf.force_valid_cpf(),
            "is_staff": True,
            "is_superuser": True,
        }
        try:
            UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            UserModel.objects.create(**fields)

        self.stdout.write(
            f"\n User credentials: \n email: {email} \n password: base \n"
        )
