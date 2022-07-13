from django_filters import rest_framework as filters

from .models import ProductsModel


class ProductsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="product_slug", lookup_expr="exact")

    class Meta:
        model = ProductsModel
        fields = ("name",)
