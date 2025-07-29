from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Payment, DiscountCode, PaymentStatus

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'reservation', 'amount', 'status', 'payment_type', 'payment_timestamp', 'created_at')
    list_filter = ('status', 'payment_type', 'payment_timestamp')
    search_fields = ('user__username', 'paypal_transaction_id', 'reservation__id')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('id', 'user', 'reservation')}),
        (_('Payment Details'), {'fields': ('amount', 'status', 'payment_type', 'paypal_transaction_id', 'payment_timestamp')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'reservation')

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'is_used', 'valid_until', 'usage_count', 'max_usage', 'created_at')
    list_filter = ('is_used', 'valid_until')
    search_fields = ('code',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('code', 'amount')}),
        (_('Usage Details'), {'fields': ('is_used', 'valid_until', 'max_usage', 'usage_count')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request)