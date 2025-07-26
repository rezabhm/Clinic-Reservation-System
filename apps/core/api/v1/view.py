from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.models import CustomUser, StaffAttendance, CustomerProfile, Comments, UserRole
from apps.core.serializers import CustomUserSerializer, StaffAttendanceSerializer, CustomerProfileSerializer, CommentsSerializer
from apps.core.api.v1.swagger_decorator import (
    admin_create_user_swagger,
    admin_retrieve_user_swagger,
    admin_update_user_swagger,
    admin_partial_update_user_swagger,
    admin_destroy_user_swagger,
    admin_list_user_swagger,
    user_retrieve_profile_swagger,
    user_update_profile_swagger,
    admin_create_attendance_swagger,
    admin_retrieve_attendance_swagger,
    admin_update_attendance_swagger,
    admin_list_attendance_swagger,
    operator_retrieve_attendance_swagger,
    operator_list_attendance_swagger,
    admin_create_customer_profile_swagger,
    admin_retrieve_customer_profile_swagger, admin_update_customer_profile_swagger,
    admin_list_customer_profile_swagger,
    user_retrieve_customer_profile_swagger, user_update_customer_profile_swagger,
    admin_create_comment_swagger,
    admin_retrieve_comment_swagger,
    admin_update_comment_swagger,
    admin_list_comment_swagger,
    admin_unreviewed_comments_swagger,
    user_create_comment_swagger,
    user_retrieve_comment_swagger,
    user_list_comment_swagger,
)

@method_decorator(name='create', decorator=admin_create_user_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_user_swagger)
@method_decorator(name='update', decorator=admin_update_user_swagger)
@method_decorator(name='partial_update', decorator=admin_partial_update_user_swagger)
@method_decorator(name='destroy', decorator=admin_destroy_user_swagger)
@method_decorator(name='list', decorator=admin_list_user_swagger)
class UserAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing CustomUser records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    queryset = CustomUser.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'role']

@method_decorator(name='retrieve', decorator=user_retrieve_profile_swagger)
@method_decorator(name='partial_update', decorator=user_update_profile_swagger)
class UserProfileAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """
    Authenticated user API ViewSet for viewing and updating their own profile.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict queryset to the authenticated user's profile."""
        return CustomUser.objects.filter(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        """Ensure user can only retrieve their own profile."""
        if str(kwargs.get('id')) != str(request.user.id):
            raise PermissionDenied(_('You can only access your own profile.'))
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Ensure user can only update their own profile."""
        if str(kwargs.get('id')) != str(request.user.id):
            raise PermissionDenied(_('You can only update your own profile.'))
        return super().partial_update(request, *args, **kwargs)

@method_decorator(name='create', decorator=admin_create_attendance_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_attendance_swagger)
@method_decorator(name='update', decorator=admin_update_attendance_swagger)
@method_decorator(name='list', decorator=admin_list_attendance_swagger)
class StaffAttendanceAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing StaffAttendance records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = StaffAttendanceSerializer
    lookup_field = 'id'
    queryset = StaffAttendance.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

@method_decorator(name='retrieve', decorator=operator_retrieve_attendance_swagger)
@method_decorator(name='list', decorator=operator_list_attendance_swagger)
class StaffAttendanceOperatorAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Operator API ViewSet for viewing their own attendance records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = StaffAttendanceSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict queryset to the authenticated operator's attendance records."""
        if self.request.user.role != UserRole.STAFF:
            raise PermissionDenied(_('Only staff members can access attendance records.'))
        return StaffAttendance.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Ensure operator can only retrieve their own attendance records."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied(_('You can only access your own attendance records.'))
        return super().retrieve(request, *args, **kwargs)

@method_decorator(name='create', decorator=admin_create_customer_profile_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_customer_profile_swagger)
@method_decorator(name='update', decorator=admin_update_customer_profile_swagger)
@method_decorator(name='list', decorator=admin_list_customer_profile_swagger)
class CustomerProfileAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing CustomerProfile records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CustomerProfileSerializer
    lookup_field = 'id'
    queryset = CustomerProfile.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['national_id', 'user__username']

@method_decorator(name='retrieve', decorator=user_retrieve_customer_profile_swagger)
@method_decorator(name='partial_update', decorator=user_update_customer_profile_swagger)
class CustomerProfileUserAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """
    Customer API ViewSet for viewing and updating their own profile.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict queryset to the authenticated customer's profile."""
        if self.request.user.role != UserRole.CUSTOMER:
            raise PermissionDenied(_('Only customers can access their profiles.'))
        return CustomerProfile.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Ensure customer can only retrieve their own profile."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied(_('You can only access your own profile.'))
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Ensure customer can only update their own profile."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied(_('You can only update your own profile.'))
        return super().partial_update(request, *args, **kwargs)

@method_decorator(name='create', decorator=admin_create_comment_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_comment_swagger)
@method_decorator(name='update', decorator=admin_update_comment_swagger)
@method_decorator(name='list', decorator=admin_list_comment_swagger)
class CommentsAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing Comments records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CommentsSerializer
    lookup_field = 'id'
    queryset = Comments.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['message', 'user__username']

    @method_decorator(admin_unreviewed_comments_swagger)
    @action(detail=False, methods=['get'])
    def unreviewed(self, request):
        """
        Retrieve a list of unreviewed comments.
        """
        serializer = self.get_serializer(Comments.get_unreviewed_Comments(), many=True)
        return Response(serializer.data)

@method_decorator(name='create', decorator=user_create_comment_swagger)
@method_decorator(name='retrieve', decorator=user_retrieve_comment_swagger)
@method_decorator(name='list', decorator=user_list_comment_swagger)
class CommentsUserAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Customer API ViewSet for submitting and viewing their own comments.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Restrict queryset to the authenticated customer's comments."""
        if self.request.user.role != UserRole.CUSTOMER:
            raise PermissionDenied(_('Only customers can submit or view their comments.'))
        return Comments.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Ensure only customers can submit comments."""
        if self.request.user.role != UserRole.CUSTOMER:
            raise PermissionDenied(_('Only customers can submit comments.'))
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Ensure customer can only retrieve their own comments."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied(_('You can only access your own comments.'))
        return super().retrieve(request, *args, **kwargs)