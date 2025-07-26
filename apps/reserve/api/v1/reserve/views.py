from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models import UserRole
from apps.reserve.models.reserve import ReservationSchedule, Reservation, PreReservation
from apps.reserve.serializers.reserve import ReservationScheduleSerializer, ReservationSerializer, PreReservationSerializer
from apps.reserve.api.v1.reserve.swagger_decorators import (
    admin_create_schedule_swagger,
    admin_retrieve_schedule_swagger,
    admin_update_schedule_swagger,
    admin_list_schedule_swagger,
    user_list_schedule_swagger,
    user_retrieve_schedule_swagger,
    user_available_schedules_swagger,
    admin_create_reservation_swagger,
    admin_retrieve_reservation_swagger,
    admin_update_reservation_swagger,
    admin_list_reservation_swagger,
    admin_unpaid_reservations_swagger,
    user_create_reservation_swagger,
    user_retrieve_reservation_swagger,
    user_list_reservation_swagger,
    operator_retrieve_reservation_swagger,
    operator_list_reservation_swagger,
    operator_mark_complete_swagger,
    admin_create_pre_reservation_swagger,
    admin_retrieve_pre_reservation_swagger,
    admin_update_pre_reservation_swagger,
    admin_list_pre_reservation_swagger,
    user_retrieve_pre_reservation_swagger,
    user_list_pre_reservation_swagger,
)

@method_decorator(name='create', decorator=admin_create_schedule_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_schedule_swagger)
@method_decorator(name='update', decorator=admin_update_schedule_swagger)
@method_decorator(name='list', decorator=admin_list_schedule_swagger)
class ReservationScheduleAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing ReservationSchedule records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ReservationScheduleSerializer
    lookup_field = 'id'
    queryset = ReservationSchedule.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['operator__username', 'date']

@method_decorator(name='retrieve', decorator=user_retrieve_schedule_swagger)
@method_decorator(name='list', decorator=user_list_schedule_swagger)
class ReservationScheduleAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Authenticated user API ViewSet for viewing available reservation schedules.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationScheduleSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict to available schedules."""
        return ReservationSchedule.objects.all()

    @method_decorator(user_available_schedules_swagger)
    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Retrieve available schedules for a specific date.
        """
        date = request.query_params.get('date')
        if not date:
            return Response({'error': 'Date parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(ReservationSchedule.get_available_schedules(date), many=True)
        return Response(serializer.data)

@method_decorator(name='create', decorator=admin_create_reservation_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_reservation_swagger)
@method_decorator(name='update', decorator=admin_update_reservation_swagger)
@method_decorator(name='list', decorator=admin_list_reservation_swagger)
class ReservationAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing Reservation records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ReservationSerializer
    lookup_field = 'id'
    queryset = Reservation.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'schedule__date']

    @method_decorator(admin_unpaid_reservations_swagger)
    @action(detail=False, methods=['get'])
    def unpaid(self, request):
        """
        Retrieve all unpaid reservations.
        """
        serializer = self.get_serializer(Reservation.get_unpaid_reservations(), many=True)
        return Response(serializer.data)

@method_decorator(name='create', decorator=user_create_reservation_swagger)
@method_decorator(name='retrieve', decorator=user_retrieve_reservation_swagger)
@method_decorator(name='list', decorator=user_list_reservation_swagger)
class UserReservationAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Customer API ViewSet for creating and viewing their own reservations.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict to the authenticated customer's reservations."""
        if self.request.user.role != UserRole.CUSTOMER:
            raise PermissionDenied(_('Only customers can access or create reservations.'))
        return Reservation.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Ensure only customers can create reservations."""
        if self.request.user.role != UserRole.CUSTOMER:
            raise PermissionDenied(_('Only customers can create reservations.'))
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Ensure customer can only access their own reservations."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied(_('You can only access your own reservations.'))
        return super().retrieve(request, *args, **kwargs)

@method_decorator(name='retrieve', decorator=operator_retrieve_reservation_swagger)
@method_decorator(name='list', decorator=operator_list_reservation_swagger)
class OperatorReservationAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Operator API ViewSet for viewing and updating their assigned reservations.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict to reservations assigned to the operator's schedule."""
        if self.request.user.role != UserRole.STAFF:
            raise PermissionDenied(_('Only staff members can access assigned reservations.'))
        return Reservation.objects.filter(schedule__operator=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Ensure operator can only access their assigned reservations."""
        instance = self.get_object()
        if instance.schedule.operator != request.user:
            raise PermissionDenied(_('You can only access your assigned reservations.'))
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(operator_mark_complete_swagger)
    @action(detail=True, methods=['patch'])
    def mark_complete(self, request, *args, **kwargs):
        """
        Allow operator to mark a reservation as completed.
        """
        instance = self.get_object()
        if instance.schedule.operator != request.user:
            raise PermissionDenied(_('You can only mark your assigned reservations as completed.'))
        instance.is_resolved = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

@method_decorator(name='create', decorator=admin_create_pre_reservation_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_pre_reservation_swagger)
@method_decorator(name='update', decorator=admin_update_pre_reservation_swagger)
@method_decorator(name='list', decorator=admin_list_pre_reservation_swagger)
class PreReservationAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing PreReservation records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = PreReservationSerializer
    lookup_field = 'id'
    queryset = PreReservation.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

@method_decorator(name='retrieve', decorator=user_retrieve_pre_reservation_swagger)
@method_decorator(name='list', decorator=user_list_pre_reservation_swagger)
class PreReservationUserAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Customer API ViewSet for viewing their own pre-reservations.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PreReservationSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict to the authenticated customer's pre-reservations."""
        if self.request.user.role != UserRole.CUSTOMER:
            raise PermissionDenied(_('Only customers can view their pre-reservations.'))
        return PreReservation.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Ensure customer can only access their own pre-reservations."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied(_('You can only access your own pre-reservations.'))
        return super().retrieve(request, *args, **kwargs)