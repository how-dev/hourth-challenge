import freezegun
import pytest
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestLogin:
    def test_login_with_empty_payload(self, api_client):
        payload = {
            "path": "/api/v1/login/",
            "data": {},
        }

        response = api_client.post(**payload)

        assert response.status_code == 400
        assert response.json() == {
            "email": ["This field is required."],
            "password": ["This field is required."],
        }

    def test_login_with_invalid_credentials(self, api_client):
        payload = {
            "path": "/api/v1/login/",
            "data": {"email": "invalid@mail.com", "password": "invalid"},
        }

        response = api_client.post(**payload)

        assert response.status_code == 404
        assert response.json() == {"detail": "Not found."}

    def test_login_with_invalid_password_and_valid_email(self, super_user, api_client):
        payload = {
            "path": "/api/v1/login/",
            "data": {"email": super_user.email, "password": "invalid"},
        }

        response = api_client.post(**payload)

        assert response.status_code == 404
        assert response.json() == {"detail": "Not found."}

    @freezegun.freeze_time("2022-1-1")
    def test_login_success(self, api_client, base_user):
        payload = {
            "path": "/api/v1/login/",
            "data": {"email": base_user.email, "password": "some_password"},
        }

        response = api_client.post(**payload)

        token = Token.objects.get(user=base_user)

        assert response.status_code == 200
        assert response.json() == {
            "document": base_user.document,
            "email": base_user.email,
            "id": base_user.id,
            "is_staff": base_user.is_staff,
            "is_superuser": base_user.is_superuser,
            "last_login": "2022-01-01T00:00:00Z",
            "name": "Some Name",
            "token": token.key,
        }
