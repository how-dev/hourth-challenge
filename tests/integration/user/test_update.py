import pytest
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestUpdateUser:
    def test_update_failed_because_is_unauthenticated(self, api_client):
        payload = {
            "path": "/api/v1/user/0/",
            "data": {},
        }

        response = api_client.patch(**payload)

        assert response.status_code == 401
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }

    def test_update_failed_because_is_invalid_credentials(self, api_client):
        payload = {
            "path": "/api/v1/user/0/",
            "data": {},
        }

        api_client.credentials(HTTP_AUTHORIZATION="Token invalid12321")

        response = api_client.patch(**payload)

        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid token."}

    def test_update_failed_because_is_staff_user(self, staff_user_logged):
        payload = {
            "path": "/api/v1/user/0/",
            "data": {},
        }

        response = staff_user_logged.patch(**payload)

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }

    def test_update_failed_because_is_base_user(self, base_user_logged):
        payload = {
            "path": "/api/v1/user/0/",
            "data": {},
        }

        response = base_user_logged.patch(**payload)

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }

    def test_update_success(self, super_user, super_user_logged):
        payload = {
            "path": f"/api/v1/user/{super_user.id}",
            "data": {"name": "Test"},
            "follow": True,
        }

        response = super_user_logged.patch(**payload)

        token = Token.objects.last()

        assert response.status_code == 200
        assert response.json() == {
            "id": token.user.id,
            "last_login": None,
            "is_superuser": super_user.is_superuser,
            "is_staff": super_user.is_staff,
            "email": super_user.email,
            "name": super_user.name,
            "document": super_user.document,
        }
