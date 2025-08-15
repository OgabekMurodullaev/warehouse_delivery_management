from rest_framework.routers import DefaultRouter
from .views import WarehouseViewSet

app_name = 'warehouse'

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)

urlpatterns = router.urls
