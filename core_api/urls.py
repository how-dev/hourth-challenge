from django.contrib import admin
from django.urls import include, path

api_prefix = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(api_prefix, include("apps.products.urls")),
    path(api_prefix, include("apps.user.urls")),
]
