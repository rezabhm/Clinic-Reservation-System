from rest_framework.routers import DefaultRouter
from apps.reserve.api.v1.reserve.views import (
    ReservationScheduleAdminAPIView,
    ReservationScheduleAPIView,
    ReservationAdminAPIView,
    UserReservationAPIView,
    OperatorReservationAPIView,
    PreReservationAdminAPIView,
    PreReservationUserAPIView,
)
from apps.reserve.api.v1.program.views import (
    OperatorShiftAdminAPIView,
    OperatorShiftOperatorAPIView,
    CancellationPeriodAdminAPIView,
    CancellationPeriodUserAPIView,
)

app_name = 'reserve'

router = DefaultRouter()


"""
reserve
"""
# Reservation Schedule Admin Routes
router.register(r'admin/schedules', ReservationScheduleAdminAPIView, basename='admin-reservation-schedule')

# Reservation Schedule User Routes
router.register(r'schedules', ReservationScheduleAPIView, basename='reservation-schedule')

# Reservation Admin Routes
router.register(r'admin/reservations', ReservationAdminAPIView, basename='admin-reservation')

# Reservation Customer Routes
router.register(r'reservations', UserReservationAPIView, basename='user-reservation')

# Reservation Operator Routes
router.register(r'operator/reservations', OperatorReservationAPIView, basename='operator-reservation')

# Pre-Reservation Admin Routes
router.register(r'admin/pre-reservations', PreReservationAdminAPIView, basename='admin-pre-reservation')

# Pre-Reservation User Routes
router.register(r'pre-reservations', PreReservationUserAPIView, basename='pre-reservation')

"""
program
"""
# Operator Shift Admin Routes
router.register(r'admin/shifts', OperatorShiftAdminAPIView, basename='admin-operator-shift')

# Operator Shift Operator Routes
router.register(r'shifts', OperatorShiftOperatorAPIView, basename='operator-shift')

# Cancellation Period Admin Routes
router.register(r'admin/cancellation-periods', CancellationPeriodAdminAPIView, basename='admin-cancellation-period')

# Cancellation Period User Routes
router.register(r'cancellation-periods', CancellationPeriodUserAPIView, basename='cancellation-period')

urlpatterns = router.urls
