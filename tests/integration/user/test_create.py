import pytest
from rest_framework.authtoken.models import Token

from apps.user.models import UserModel


@pytest.mark.django_db
class TestCreateUser:
    def test_create_failed_because_is_unauthenticated(self, api_client):
        payload = {
            "path": "/api/v1/user/",
            "data": {},
        }

        response = api_client.post(**payload)

        assert response.status_code == 401
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }

    def test_create_failed_because_is_invalid_credentials(self, api_client):
        payload = {
            "path": "/api/v1/user/",
            "data": {},
        }

        api_client.credentials(HTTP_AUTHORIZATION="Token invalid12321")

        response = api_client.post(**payload)

        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid token."}

    def test_create_failed_because_is_staff_user(self, staff_user_logged):
        payload = {
            "path": "/api/v1/user/",
            "data": {},
        }

        response = staff_user_logged.post(**payload)

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }

    def test_create_failed_because_is_base_user(self, base_user_logged):
        payload = {
            "path": "/api/v1/user/",
            "data": {},
        }

        response = base_user_logged.post(**payload)

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }

    def test_create_success(self, super_user_logged):
        payload = {
            "path": "/api/v1/user/",
            "data": {
                "email": "test@mail.com",
                "password": "test",
                "name": "Test",
                "document": "90078144191",  # 4Devs
            },
        }

        response = super_user_logged.post(**payload)

        user = UserModel.objects.get(email="test@mail.com")
        token = Token.objects.get(user=user)

        assert response.status_code == 201
        assert response.json() == {
            "id": user.id,
            "last_login": None,
            "is_superuser": False,
            "is_staff": False,
            "email": "test@mail.com",
            "name": "Test",
            "document": "90078144191",
            "token": token.key,
        }
