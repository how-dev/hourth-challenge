from rest_framework import serializers

from .models import UserModel


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"write_only": True},
            "date_joined": {"write_only": True},
        }
