import factory
from django.contrib.auth.hashers import make_password

from apps.user.models import UserModel


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserModel

    email = factory.Faker("email")
    name = "Some Name"
    document = "90078144191"  # 4Devs
    password = make_password("some_password")
