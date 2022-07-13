from rest_framework.permissions import BasePermission

from apps.user.exceptions import UserPermissionException


class UserPermissions(BasePermission):
    protected_methods = ("POST", "GET", "PATCH", "PUT", "DELETE")

    @staticmethod
    def is_retrieve(request):
        path = request.path
        user_id = path[13:].replace("/", "")

        return user_id.isnumeric()

    def get_retrieve_id(self, request):
        if not self.is_retrieve(request):
            return 0

        path = request.path
        user_id = path[13:].replace("/", "")

        return int(user_id)

    @staticmethod
    def is_authenticated_but_not_allowed_to_create(request):
        method = request.method
        user = request.user
        is_superuser = user.is_superuser
        is_authenticated = user.is_authenticated
        is_post = method == "POST"

        if is_authenticated and not is_superuser and is_post:
            raise UserPermissionException

    def is_authenticated_and_method_in_protect_methods(self, request):
        method = request.method
        user = request.user

        if not user.is_authenticated and method in self.protected_methods:
            raise UserPermissionException

    def is_superuser_to_all_get(self, request):
        method = request.method
        user = request.user
        is_retrieve = self.is_retrieve(request)
        is_get = method == "GET"
        is_superuser = user.is_superuser

        if not is_retrieve and is_get and not is_superuser:
            raise UserPermissionException

    def is_self_retrieve(self, request):
        user = request.user
        is_superuser = user.is_superuser
        is_retrieve = self.is_retrieve(request)
        is_self_retrieve = self.get_retrieve_id(request) != user.id

        if is_retrieve and is_self_retrieve and not is_superuser:
            raise UserPermissionException

    def has_permission(self, request, _):
        try:
            self.is_authenticated_but_not_allowed_to_create(request)
            self.is_authenticated_and_method_in_protect_methods(request)
            self.is_superuser_to_all_get(request)
            self.is_self_retrieve(request)
            return True
        except UserPermissionException:
            return False
