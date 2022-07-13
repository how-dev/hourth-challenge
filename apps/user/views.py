import json

from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet, ViewSet

from services.user_flow import ResetToken

from .filters import UserFilter
from .models import UserModel
from .permissions import UserPermissions
from .serializers import LoginSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.order_by("id").filter(is_active=True)
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermissions]
    throttle_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    @method_decorator(cache_page(20, key_prefix="list_users"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        cache.set("list_users", json.dumps(serializer.data))
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["password"] = make_password(
            serializer.validated_data["password"]
        )
        self.perform_create(serializer)

        user = UserModel.objects.get(id=serializer.data["id"])
        token = Token.objects.create(user=user)
        headers = self.get_success_headers(serializer.data)

        data = serializer.data
        data["token"] = token.key

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginViewSet(ViewSet):
    queryset = UserModel.objects.all()

    @staticmethod
    def create(request):
        data = request.data

        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = data["email"]
        password = data["password"]

        user = get_object_or_404(UserModel, email=email)

        is_valid_password = check_password(password, user.password)

        if is_valid_password:
            user.last_login = timezone.now()
            user.save()
            data = UserSerializer(user).data

            token = Token.objects.get_or_create(user=user)[0]
            reset_token = ResetToken(token.key, user, 1)
            token = reset_token.reset_token()
            data["token"] = token.key

            return Response(data)
        else:
            return Response(
                {"detail": _("Not found.")}, status=status.HTTP_404_NOT_FOUND
            )
