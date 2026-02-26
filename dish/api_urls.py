"""料理APIのURL定義。"""
from rest_framework.routers import DefaultRouter

from .api_views import CategoryViewSet, DishViewSet


router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="api-category")
router.register("dishes", DishViewSet, basename="api-dish")

urlpatterns = router.urls

