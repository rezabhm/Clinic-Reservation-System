from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, StaffAttendance, CustomerProfile, Comments

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')

@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry_timestamp', 'exit_timestamp', 'has_exited', 'created_at')
    list_filter = ('has_exited', 'entry_timestamp')
    search_fields = ('user__username', 'user__email')
    ordering = ('-entry_timestamp',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('user', 'id')}),
        (_('Attendance Details'), {'fields': ('entry_timestamp', 'exit_timestamp', 'has_exited')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'national_id', 'is_premium', 'last_visit_date', 'created_at')
    list_filter = ('is_premium', 'has_medical_history', 'has_drug_history')
    search_fields = ('user__username', 'national_id', 'primary_physician')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('user', 'national_id')}),
        (_('Profile Details'), {'fields': ('address', 'house_number', 'has_medical_history', 'has_drug_history', 'primary_physician', 'is_premium', 'offline_appointments', 'last_visit_date')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_preview', 'is_reviewed', 'created_at')
    list_filter = ('is_reviewed', 'created_at')
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('user', 'id')}),
        (_('Comment Details'), {'fields': ('message', 'is_reviewed')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 25

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = _('Message Preview')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')