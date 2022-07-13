import pytest

from tests.factories.sale import SalesFactory


@pytest.mark.django_db
class TestListProducts:
    def test_list_failed_because_is_unauthenticated(self, api_client):
        payload = {"path": "/api/v1/products/"}

        response = api_client.get(**payload)

        assert response.status_code == 401
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }

    def test_list_failed_because_is_invalid_credentials(self, api_client):
        payload = {"path": "/api/v1/products/"}

        api_client.credentials(HTTP_AUTHORIZATION="Token invalid12321")

        response = api_client.get(**payload)

        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid token."}

    def test_list_failed_because_is_staff_user(self, staff_user_logged):
        payload = {"path": "/api/v1/products/"}

        response = staff_user_logged.get(**payload)

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }

    def test_list_failed_because_is_base_user(self, base_user_logged):
        payload = {"path": "/api/v1/products/"}

        response = base_user_logged.get(**payload)

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }

    def test_list_success(self, super_user_logged):
        payload = {"path": "/api/v1/products/"}

        response = super_user_logged.get(**payload)

        assert response.status_code == 200

    def test_list_success_filter_by_product_slug(self, base_product, super_user_logged):
        sale = SalesFactory(products=base_product)
        SalesFactory.create_batch(3, products=base_product)

        sale_date = str(sale.insertion_date)

        payload = {"path": f"/api/v1/products/?name={base_product.product_slug}"}

        response = super_user_logged.get(**payload)

        assert response.status_code == 200
        assert response.json() == {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": base_product.id,
                    "product_url__image": None,
                    "product_url": base_product.url,
                    "product_url__created_at": str(base_product.insertion_date),
                    "sales": [{sale_date: base_product.sales_amount}],
                }
            ],
        }

    def test_list_success_consult_date(self, base_product, super_user_logged):
        sale = SalesFactory(products=base_product)
        SalesFactory.create_batch(3, products=base_product)

        consult_date = str(sale.insertion_date)

        payload = {
            "path": f"/api/v1/products/?name={base_product.product_slug}&consult_date={consult_date}"
        }

        response = super_user_logged.get(**payload)

        assert response.status_code == 200
        assert response.json() == {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": base_product.id,
                    "product_url__image": None,
                    "product_url": base_product.url,
                    "product_url__created_at": str(base_product.insertion_date),
                    "consult_date": consult_date,
                    "sales_on_the_day": base_product.sales_amount,
                }
            ],
        }
