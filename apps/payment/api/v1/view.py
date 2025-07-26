from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.payment.models import Payment, DiscountCode
from apps.payment.serializers import PaymentSerializer, DiscountCodeSerializer
from apps.payment.api.v1.swagger_decorator import (
    admin_create_payment_swagger,
    admin_retrieve_payment_swagger,
    admin_update_payment_swagger,
    admin_list_payment_swagger,
    admin_pending_payments_swagger,
    user_create_payment_swagger,
    user_retrieve_payment_swagger,
    user_list_payment_swagger,
    admin_create_discount_code_swagger,
    admin_retrieve_discount_code_swagger,
    admin_update_discount_code_swagger,
    admin_list_discount_code_swagger,
    user_list_discount_code_swagger,
    user_retrieve_discount_code_swagger,
    user_valid_codes_swagger,
)

@method_decorator(name='create', decorator=admin_create_payment_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_payment_swagger)
@method_decorator(name='update', decorator=admin_update_payment_swagger)
@method_decorator(name='list', decorator=admin_list_payment_swagger)
class PaymentAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing Payment records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = PaymentSerializer
    lookup_field = 'id'
    queryset = Payment.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'paypal_transaction_id']

    @method_decorator(admin_pending_payments_swagger)
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Retrieve all pending payments.
        """
        serializer = PaymentSerializer(Payment.get_pending_payments(), many=True)
        return Response(serializer.data)

@method_decorator(name='create', decorator=user_create_payment_swagger)
@method_decorator(name='retrieve', decorator=user_retrieve_payment_swagger)
@method_decorator(name='list', decorator=user_list_payment_swagger)
class PaymentCustomerAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Customer API ViewSet for creating and viewing their own payments.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict to the authenticated customer's payments."""
        if self.request.user.role != UserRole.CUSTOMER:
            raise PermissionDenied(_('Only customers can access or create payments.'))
        return Payment.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Ensure only customers can create payments."""
        if self.request.user.role != UserRole.CUSTOMER:
            raise PermissionDenied(_('Only customers can create payments.'))
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Ensure customer can only retrieve their own payments."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied(_('You can only access your own payments.'))
        return super().retrieve(request, *args, **kwargs)

@method_decorator(name='create', decorator=admin_create_discount_code_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_discount_code_swagger)
@method_decorator(name='update', decorator=admin_update_discount_code_swagger)
@method_decorator(name='list', decorator=admin_list_discount_code_swagger)
class DiscountCodeAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing DiscountCode records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = DiscountCodeSerializer
    lookup_field = 'code'
    queryset = DiscountCode.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields=['code']

@method_decorator(name='retrieve', decorator=user_retrieve_discount_code_swagger)
@method_decorator(name='list', decorator=user_list_discount_code_swagger)
class DiscountCodeUserAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Authenticated user API ViewSet for viewing available discount codes.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DiscountCodeSerializer
    lookup_field = 'code'

    def get_queryset(self):
        """Restrict to valid, unused discount codes."""
        return DiscountCode.objects.filter(is_used=False, valid_until__gte=timezone.now())

    @method_decorator(user_valid_codes_swagger)
    @action(detail=False, methods=['get'])
    def valid(self, request):
        """
        Retrieve all valid discount codes.
        """
        serializer = self.get_serializer(DiscountCode.get_valid_codes(), many=True)
        return Response(serializer.data)