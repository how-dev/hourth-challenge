from rest_framework.routers import DefaultRouter

from .views import UserLoginViewSet, UserViewSet

router = DefaultRouter()
router.register("login", UserLoginViewSet)
router.register("user", UserViewSet)

urlpatterns = router.urls
