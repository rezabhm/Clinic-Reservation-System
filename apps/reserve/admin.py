from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import OperatorShift, CancellationPeriod, ReservationSchedule, Reservation, PreReservation

@admin.register(OperatorShift)
class OperatorShiftAdmin(admin.ModelAdmin):
    list_display = ('operator', 'operator_name', 'shift_date', 'period', 'created_at')
    list_filter = ('period', 'shift_date')
    search_fields = ('operator__username', 'operator_name')
    ordering = ('-shift_date',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('id', 'operator', 'operator_name')}),
        (_('Shift Details'), {'fields': ('shift_date', 'period')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('operator')

@admin.register(CancellationPeriod)
class CancellationPeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'created_at')
    list_filter = ('start_time', 'end_time')
    search_fields = ('id',)
    ordering = ('-start_time',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('id',)}),
        (_('Cancellation Period'), {'fields': ('start_time', 'end_time')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request)

@admin.register(ReservationSchedule)
class ReservationScheduleAdmin(admin.ModelAdmin):
    list_display = ('operator', 'date', 'period', 'time_slot', 'duration', 'created_at')
    list_filter = ('period', 'date', 'time_slot')
    search_fields = ('operator__username',)
    ordering = ('-date', 'time_slot')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('id', 'operator')}),
        (_('Schedule Details'), {'fields': ('date', 'period', 'time_slot', 'duration')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('operator')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'schedule', 'laser_area', 'reservation_type', 'is_paid', 'total_price', 'final_amount', 'created_at')
    list_filter = ('reservation_type', 'is_paid', 'is_charged', 'is_online', 'used_discount_code')
    search_fields = ('user__username', 'id', 'laser_area__name', 'discount_code__code')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('id', 'user', 'schedule', 'laser_area')}),
        (_('Reservation Details'), {'fields': ('reservation_type', 'is_online', 'is_charged', 'is_paid', 'session_number')}),
        (_('Pricing'), {'fields': ('total_price', 'final_amount', 'used_discount_code', 'discount_code')}),
        (_('Timestamps'), {'fields': ('reservation_timestamp', 'request_timestamp', 'created_at', 'updated_at')}),
        (_('Related Schedules'), {'fields': ('laser_area_schedules',)}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'schedule', 'laser_area', 'discount_code').prefetch_related('laser_area_schedules')

@admin.register(PreReservation)
class PreReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'laser_area_schedule', 'session_count', 'last_session_date', 'created_at')
    list_filter = ('last_session_date',)
    search_fields = ('user__username', 'id', 'laser_area_schedule__laser_area__name')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('id', 'user', 'laser_area_schedule')}),
        (_('Pre-Reservation Details'), {'fields': ('session_count', 'last_session_date')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'laser_area_schedule__laser_area')