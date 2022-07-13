import pytest
from rest_framework.test import APIClient

from tests.factories.product import ProductsFactory
from tests.factories.sale import SalesFactory
from tests.factories.token import TokenFactory
from tests.factories.user import UserFactory


@pytest.fixture()
def base_sale():
    return SalesFactory()


@pytest.fixture()
def base_product():
    return ProductsFactory()


@pytest.fixture()
def base_user():
    return UserFactory()


@pytest.fixture()
def staff_user():
    return UserFactory(is_staff=True)


@pytest.fixture()
def super_user():
    return UserFactory(is_staff=True, is_superuser=True)


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def token_super_user(super_user):
    return TokenFactory(user=super_user)


@pytest.fixture()
def token_staff_user(staff_user):
    return TokenFactory(user=staff_user)


@pytest.fixture()
def token_base_user(base_user):
    return TokenFactory(user=base_user)


@pytest.fixture()
def super_user_logged(token_super_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token_super_user}")
    return client


@pytest.fixture()
def staff_user_logged(token_staff_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff_user}")
    return client


@pytest.fixture()
def base_user_logged(token_base_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token_base_user}")
    return client
