import pytest


@pytest.mark.django_db
class TestRetrieveUser:
    def test_retrieve_failed_because_is_unauthenticated(self, api_client):
        payload = {"path": "/api/v1/user/0/"}

        response = api_client.get(**payload)

        assert response.status_code == 401
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }

    def test_retrieve_failed_because_is_invalid_credentials(self, api_client):
        payload = {"path": "/api/v1/user/0/"}

        api_client.credentials(HTTP_AUTHORIZATION="Token invalid12321")

        response = api_client.get(**payload)

        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid token."}

    def test_retrieve_failed_because_is_staff_user(self, staff_user_logged):
        payload = {"path": "/api/v1/user/0/"}

        response = staff_user_logged.get(**payload)

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }

    def test_retrieve_failed_because_is_base_user(self, base_user_logged):
        payload = {"path": "/api/v1/user/0/"}

        response = base_user_logged.get(**payload)

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }

    def test_retrieve_success(self, super_user, super_user_logged):
        payload = {"path": f"/api/v1/user/{super_user.id}", "follow": True}

        response = super_user_logged.get(**payload)

        assert response.status_code == 200
