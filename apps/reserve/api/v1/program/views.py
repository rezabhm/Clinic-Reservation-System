from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models import UserRole
from apps.reserve.models.program import OperatorShift, CancellationPeriod
from apps.reserve.serializers.program import OperatorShiftSerializer, CancellationPeriodSerializer
from apps.reserve.api.v1.program.swagger_decorators import (
    admin_create_shift_swagger,
    admin_retrieve_shift_swagger,
    admin_update_shift_swagger,
    admin_list_shift_swagger,
    operator_retrieve_shift_swagger,
    operator_list_shift_swagger,
    operator_active_shifts_swagger,
    admin_create_cancellation_period_swagger,
    admin_retrieve_cancellation_period_swagger,
    admin_update_cancellation_period_swagger,
    admin_list_cancellation_period_swagger,
    user_retrieve_cancellation_period_swagger,
    user_list_cancellation_period_swagger,
)

@method_decorator(name='create', decorator=admin_create_shift_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_shift_swagger)
@method_decorator(name='update', decorator=admin_update_shift_swagger)
@method_decorator(name='list', decorator=admin_list_shift_swagger)
class OperatorShiftAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing OperatorShift records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = OperatorShiftSerializer
    lookup_field = 'id'
    queryset = OperatorShift.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['operator__username', 'date']

@method_decorator(name='retrieve', decorator=operator_retrieve_shift_swagger)
@method_decorator(name='list', decorator=operator_list_shift_swagger)
class OperatorShiftOperatorAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Operator API ViewSet for viewing their own shifts.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OperatorShiftSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict queryset to the authenticated operator's shifts."""
        if self.request.user.role != UserRole.STAFF:
            raise PermissionDenied(_('Only staff members can access their shifts.'))
        return OperatorShift.objects.filter(operator=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Ensure operator can only retrieve their own shifts."""
        instance = self.get_object()
        if instance.operator != request.user:
            raise PermissionDenied(_('You can only access your own shifts.'))
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(operator_active_shifts_swagger)
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Retrieve active shifts for the authenticated operator.
        """
        serializer = self.get_serializer(OperatorShift.get_active_shifts(self.request.user), many=True)
        return Response(serializer.data)

@method_decorator(name='create', decorator=admin_create_cancellation_period_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_cancellation_period_swagger)
@method_decorator(name='update', decorator=admin_update_cancellation_period_swagger)
@method_decorator(name='list', decorator=admin_list_cancellation_period_swagger)
class CancellationPeriodAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing CancellationPeriod records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CancellationPeriodSerializer
    lookup_field = 'id'
    queryset = CancellationPeriod.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['laser_area__name']

@method_decorator(name='retrieve', decorator=user_retrieve_cancellation_period_swagger)
@method_decorator(name='list', decorator=user_list_cancellation_period_swagger)
class CancellationPeriodUserAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Authenticated user API ViewSet for viewing active cancellation periods.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CancellationPeriodSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict queryset to active cancellation periods."""
        return CancellationPeriod.objects.filter()