from rest_framework.routers import DefaultRouter
from apps.core.api.v1.view import (
    UserAdminAPIView,
    UserProfileAPIView,
    StaffAttendanceAdminAPIView,
    StaffAttendanceOperatorAPIView,
    CustomerProfileAdminAPIView,
    CustomerProfileUserAPIView,
    CommentsAdminAPIView,
    CommentsUserAPIView,
)

app_name = 'core'

router = DefaultRouter()

# User Admin Routes
router.register(r'admin/users', UserAdminAPIView, basename='admin-user')

# User Profile Routes
router.register(r'users/profile', UserProfileAPIView, basename='user-profile')

# Staff Attendance Admin Routes
router.register(r'admin/staff-attendance', StaffAttendanceAdminAPIView, basename='admin-staff-attendance')

# Staff Attendance Operator Routes
router.register(r'operator/staff-attendance', StaffAttendanceOperatorAPIView, basename='operator-staff-attendance')

# Customer Profile Admin Routes
router.register(r'admin/customer-profiles', CustomerProfileAdminAPIView, basename='admin-customer-profile')

# Customer Profile User Routes
router.register(r'customer-profiles', CustomerProfileUserAPIView, basename='customer-profile')

# Comments Admin Routes
router.register(r'admin/comments', CommentsAdminAPIView, basename='admin-comment')

# Comments User Routes
router.register(r'comments', CommentsUserAPIView, basename='comment')

urlpatterns = router.urls
