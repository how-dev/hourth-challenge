import factory
from rest_framework.authtoken.models import Token

from tests.factories.user import UserFactory


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token

    user = factory.SubFactory(UserFactory)
