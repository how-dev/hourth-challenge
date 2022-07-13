import json

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.user.permissions import UserPermissions

from .filters import ProductsFilter
from .models import ProductsModel
from .serializers import ProductsSerializer


class ProductsViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermissions]
    queryset = ProductsModel.objects.filter(is_active=True).order_by("id")
    filter_backends = [DjangoFilterBackend]
    throttle_classes = [UserRateThrottle]
    filterset_class = ProductsFilter

    @method_decorator(cache_page(20, key_prefix="list_products"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        context = {"consult_date": request.query_params.get("consult_date")}

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, context=context, many=True)
        cache.set("list_products", json.dumps(serializer.data))
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        context = {"consult_date": request.query_params.get("consult_date")}
        instance = self.get_object()
        serializer = self.get_serializer(instance, context=context)
        return Response(serializer.data)
