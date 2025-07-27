from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.lazer_area.models import LaserArea, LaserAreaSchedule
from apps.lazer_area.serializers import LaserAreaSerializer, LaserAreaScheduleSerializer
from apps.lazer_area.api.v1.swagger_decorator import (
    admin_create_laser_area_swagger,
    admin_retrieve_laser_area_swagger,
    admin_update_laser_area_swagger, admin_list_laser_area_swagger,
    admin_destroy_laser_area_swagger,
    user_list_laser_area_swagger,
    user_retrieve_laser_area_swagger,
    admin_create_laser_schedule_swagger,
    admin_retrieve_laser_schedule_swagger,
    admin_update_laser_schedule_swagger,
    admin_list_laser_schedule_swagger,
    user_list_laser_schedule_swagger,
    user_retrieve_laser_schedule_swagger,
    user_active_schedules_swagger,
)

@method_decorator(name='create', decorator=admin_create_laser_area_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_laser_area_swagger)
@method_decorator(name='update', decorator=admin_update_laser_area_swagger)
@method_decorator(name='destroy', decorator=admin_destroy_laser_area_swagger)
@method_decorator(name='list', decorator=admin_list_laser_area_swagger)
class LaserAreaAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing LaserArea records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]
    serializer_class = LaserAreaSerializer
    lookup_field = 'name'
    queryset = LaserArea.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

@method_decorator(name='retrieve', decorator=user_retrieve_laser_area_swagger)
@method_decorator(name='list', decorator=user_list_laser_area_swagger)
class LaserAreaUserAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Authenticated user API ViewSet for viewing active LaserArea records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LaserAreaSerializer
    lookup_field = 'name'

    def get_queryset(self):
        """Restrict queryset to active laser areas."""
        return LaserArea.objects.filter(is_active=True)

@method_decorator(name='create', decorator=admin_create_laser_schedule_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_laser_schedule_swagger)
@method_decorator(name='update', decorator=admin_update_laser_schedule_swagger)
@method_decorator(name='list', decorator=admin_list_laser_schedule_swagger)
class LaserAreaScheduleAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing LaserAreaSchedule records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = LaserAreaScheduleSerializer
    lookup_field = 'id'
    queryset = LaserAreaSchedule.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['laser_area__name']

@method_decorator(name='retrieve', decorator=user_retrieve_laser_schedule_swagger)
@method_decorator(name='list', decorator=user_list_laser_schedule_swagger)
class LaserAreaScheduleUserAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Authenticated user API ViewSet for viewing available laser area schedules.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LaserAreaScheduleSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict queryset to schedules with non-null start times."""
        return LaserAreaSchedule.objects.filter(start_time__isnull=False)

    @method_decorator(user_active_schedules_swagger)
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Retrieve all active laser area schedules.
        """
        serializer = self.get_serializer(LaserAreaSchedule.get_active_schedules(), many=True)
        return Response(serializer.data)