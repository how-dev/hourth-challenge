import pytest


@pytest.mark.django_db
class TestListUser:
    def test_list_failed_because_is_unauthenticated(self, api_client):
        payload = {"path": "/api/v1/user/"}

        response = api_client.get(**payload)

        assert response.status_code == 401
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }

    def test_list_failed_because_is_invalid_credentials(self, api_client):
        payload = {"path": "/api/v1/user/"}

        api_client.credentials(HTTP_AUTHORIZATION="Token invalid12321")

        response = api_client.get(**payload)

        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid token."}

    def test_list_failed_because_is_staff_user(self, staff_user_logged):
        payload = {"path": "/api/v1/user/"}

        response = staff_user_logged.get(**payload)

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }

    def test_list_failed_because_is_base_user(self, base_user_logged):
        payload = {"path": "/api/v1/user/"}

        response = base_user_logged.get(**payload)

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }

    def test_list_success(self, super_user_logged):
        payload = {"path": "/api/v1/user/"}

        response = super_user_logged.get(**payload)

        assert response.status_code == 200
