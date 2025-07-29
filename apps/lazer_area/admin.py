from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import LaserArea, LaserAreaSchedule

@admin.register(LaserArea)
class LaserAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_price', 'is_active', 'operate_time', 'deadline_reset', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'current_price')}),
        (_('Operational Settings'), {'fields': ('deadline_reset', 'is_active', 'operate_time')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

@admin.register(LaserAreaSchedule)
class LaserAreaScheduleAdmin(admin.ModelAdmin):
    list_display = ('laser_area', 'price', 'start_time', 'end_time', 'operate_time', 'created_at')
    list_filter = ('laser_area', 'start_time')
    search_fields = ('laser_area__name',)
    ordering = ('-start_time',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('laser_area', 'id')}),
        (_('Schedule Details'), {'fields': ('price', 'start_time', 'end_time', 'operate_time')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('laser_area')