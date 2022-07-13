from rest_framework.routers import DefaultRouter

from .views import ProductsViewSet

router = DefaultRouter()

router.register("products", ProductsViewSet)

urlpatterns = router.urls
