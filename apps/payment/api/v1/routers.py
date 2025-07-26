from rest_framework.routers import DefaultRouter
from apps.payment.api.v1.view import (
    PaymentAdminAPIView,
    PaymentCustomerAPIView,
    DiscountCodeAdminAPIView,
    DiscountCodeUserAPIView,
)

app_name = 'payment'

router = DefaultRouter()

# Payment Admin Routes
router.register(r'admin/payments', PaymentAdminAPIView, basename='admin-payment')

# Payment Customer Routes
router.register(r'payments', PaymentCustomerAPIView, basename='payment')

# Discount Code Admin Routes
router.register(r'admin/discount-codes', DiscountCodeAdminAPIView, basename='admin-discount-code')

# Discount Code User Routes
router.register(r'discount-codes', DiscountCodeUserAPIView, basename='discount-code')

urlpatterns = router.urls
