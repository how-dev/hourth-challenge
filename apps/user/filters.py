from django_filters import rest_framework as filters

from .models import UserModel


class UserFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id")
    last_login = filters.DateTimeFilter(field_name="last_login", lookup_expr="gte")
    is_active = filters.BooleanFilter(field_name="is_active")
    date_joined = filters.DateTimeFilter(field_name="date_joined", lookup_expr="gte")
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    document = filters.CharFilter(field_name="document", lookup_expr="icontains")

    class Meta:
        model = UserModel
        fields = [
            "id",
            "last_login",
            "is_active",
            "date_joined",
            "email",
            "name",
            "document",
        ]
