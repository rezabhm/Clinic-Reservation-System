from rest_framework.routers import DefaultRouter
from apps.lazer_area.api.v1.view import (
    LaserAreaAdminAPIView,
    LaserAreaUserAPIView,
    LaserAreaScheduleAdminAPIView,
    LaserAreaScheduleUserAPIView,
)

app_name = 'lazerapp'

router = DefaultRouter()

# Laser Area Admin Routes
router.register(r'admin/laser-areas', LaserAreaAdminAPIView, basename='admin-laser-area')

# Laser Area User Routes
router.register(r'laser-areas', LaserAreaUserAPIView, basename='laser-area')

# Laser Area Schedule Admin Routes
router.register(r'admin/laser-schedules', LaserAreaScheduleAdminAPIView, basename='admin-laser-schedule')

# Laser Area Schedule User Routes
router.register(r'laser-schedules', LaserAreaScheduleUserAPIView, basename='laser-schedule')

urlpatterns = router.urls
