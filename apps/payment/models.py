from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging
from uuid import uuid4
from typing import List
from django.conf import settings
from django.core.validators import MinValueValidator

from apps.core.models import BaseModel

# Configure logging for better debugging and monitoring
logger = logging.getLogger(__name__)


class PaymentStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    COMPLETED = 'COMPLETED', _('Completed')
    FAILED = 'FAILED', _('Failed')
    REFUNDED = 'REFUNDED', _('Refunded')
    CANCELLED = 'CANCELLED', _('Cancelled')


class PaymentType(models.TextChoices):
    PAYPAL = 'PAYPAL', _('PayPal')
    CREDIT_CARD = 'CREDIT_CARD', _('Credit Card')
    BANK_TRANSFER = 'BANK_TRANSFER', _('Bank Transfer')


class Payment(BaseModel):
    """
    Model to store payment transactions with PayPal integration.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name=_("Payment ID"),
        help_text=_("Unique identifier for the payment transaction")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name=_("User"),
        help_text=_("User who initiated the payment")
    )
    reservation = models.ForeignKey(
        'reserve.Reservation',
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name=_("Reservation"),
        help_text=_("Associated reservation for this payment")
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        verbose_name=_("Amount"),
        help_text=_("Total payment amount")
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name=_("Payment Status"),
        help_text=_("Current status of the payment")
    )
    payment_type = models.CharField(
        max_length=20,
        choices=PaymentType.choices,
        default=PaymentType.PAYPAL,
        verbose_name=_("Payment Type"),
        help_text=_("Method used for the payment")
    )
    paypal_transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("PayPal Transaction ID"),
        help_text=_("PayPal transaction identifier")
    )
    payment_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Payment Timestamp"),
        help_text=_("Timestamp when payment was processed")
    )

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        indexes = [
            models.Index(fields=['user', 'payment_timestamp']),
            models.Index(fields=['status']),
            models.Index(fields=['paypal_transaction_id']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['paypal_transaction_id'],
                condition=models.Q(paypal_transaction_id__isnull=False),
                name='unique_paypal_transaction_id'
            ),
        ]

    def __str__(self) -> str:
        return f"Payment {self.id} - {self.user.username} ({self.status})"

    def clean(self) -> None:
        """Validate payment fields."""
        if self.amount < 0:
            raise ValidationError(_('Payment amount cannot be negative'))
        if self.status not in PaymentStatus.values:
            raise ValidationError(_('Invalid payment status'))
        if self.payment_type not in PaymentType.values:
            raise ValidationError(_('Invalid payment type'))
        if self.payment_type == PaymentType.PAYPAL and not self.paypal_transaction_id:
            raise ValidationError(_('PayPal transaction ID is required for PayPal payments'))

    @classmethod
    def get_pending_payments(cls) -> List['Payment']:
        """Retrieve all pending payments."""
        try:
            return list(cls.objects.filter(status=PaymentStatus.PENDING))
        except Exception as e:
            logger.error(f"Error retrieving pending payments: {str(e)}")
            return []

    @classmethod
    def get_user_payments(cls, user_id: int) -> List['Payment']:
        """Retrieve all payments for a specific user."""
        try:
            return list(cls.objects.filter(user_id=user_id))
        except Exception as e:
            logger.error(f"Error retrieving payments for user {user_id}: {str(e)}")
            return []


class DiscountCode(BaseModel):
    """
    Model to store discount codes for payments.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_("Discount Code"),
        help_text=_("Unique code for the discount (max 10 characters)")
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        verbose_name=_("Discount Amount"),
        help_text=_("Discount amount to be applied")
    )
    is_used = models.BooleanField(
        default=False,
        verbose_name=_("Is Used"),
        help_text=_("Indicates if the discount code has been used")
    )
    valid_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Valid Until"),
        help_text=_("Expiration date of the discount code")
    )
    max_usage = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Maximum Usage"),
        help_text=_("Maximum number of times the code can be used")
    )
    usage_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Usage Count"),
        help_text=_("Number of times the code has been used")
    )

    class Meta:
        verbose_name = _("Discount Code")
        verbose_name_plural = _("Discount Codes")
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_used']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['code'], name='unique_discount_code'),
        ]

    def __str__(self) -> str:
        return f"{self.code} ({'Used' if self.is_used else 'Active'})"

    def clean(self) -> None:
        """Validate discount code fields."""
        if not self.code.strip():
            raise ValidationError(_('Discount code cannot be empty'))
        if self.amount < 0:
            raise ValidationError(_('Discount amount cannot be negative'))
        if self.usage_count > self.max_usage:
            raise ValidationError(_('Usage count cannot exceed maximum usage'))
        if self.valid_until and self.valid_until < timezone.now():
            raise ValidationError(_('Discount code cannot have an expired validity date'))

    def apply_discount(self, payment: 'Payment') -> None:
        """Apply discount to a payment and update usage."""
        if self.is_used or self.usage_count >= self.max_usage:
            raise ValidationError(_('Discount code is already used or exhausted'))
        if self.valid_until and self.valid_until < timezone.now():
            raise ValidationError(_('Discount code has expired'))

        try:
            payment.amount -= self.amount
            if payment.amount < 0:
                raise ValidationError(_('Discount cannot exceed payment amount'))
            self.usage_count += 1
            if self.usage_count >= self.max_usage:
                self.is_used = True
            self.save()
            payment.save()
            logger.info(f"Discount code {self.code} applied to payment {payment.id}")
        except Exception as e:
            logger.error(f"Error applying discount code {self.code}: {str(e)}")
            raise

    @classmethod
    def get_valid_codes(cls) -> List['DiscountCode']:
        """Retrieve all valid and unused discount codes."""
        try:
            return list(cls.objects.filter(is_used=False, valid_until__gte=timezone.now()))
        except Exception as e:
            logger.error(f"Error retrieving valid discount codes: {str(e)}")
            return []