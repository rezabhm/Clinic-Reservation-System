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

class TimeSlot(models.TextChoices):
    SLOT_8_10 = '8-10', _('8:00-10:00')
    SLOT_10_12 = '10-12', _('10:00-12:00')
    SLOT_12_14 = '12-14', _('12:00-14:00')
    SLOT_15_17 = '15-17', _('15:00-17:00')
    SLOT_17_19 = '17-19', _('17:00-19:00')
    SLOT_19_21 = '19-21', _('19:00-21:00')
    SLOT_21_23 = '21-23', _('21:00-23:00')
    SLOT_23_1 = '23-1', _('23:00-01:00')
    SLOT_1_3 = '1-3', _('01:00-03:00')
    SLOT_3_5 = '3-5', _('03:00-05:00')

class DayPeriod(models.TextChoices):
    MORNING = 'MORNING', _('Morning')
    AFTERNOON = 'AFTERNOON', _('Afternoon')

class ReservationType(models.TextChoices):
    STANDARD = 'STANDARD', _('Standard')
    PREMIUM = 'PREMIUM', _('Premium')

class ReservationSchedule(BaseModel):
    """
    Model to store reservation schedules for laser treatments.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name=_("Schedule ID"),
        help_text=_("Unique identifier for the schedule")
    )
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='schedules',
        verbose_name=_("Operator"),
        help_text=_("Operator assigned to this schedule")
    )
    date = models.DateField(
        verbose_name=_("Date"),
        help_text=_("Date of the reservation schedule")
    )
    period = models.CharField(
        max_length=20,
        choices=DayPeriod.choices,
        verbose_name=_("Day Period"),
        help_text=_("Time period of the day (morning or afternoon)")
    )
    time_slot = models.CharField(
        max_length=10,
        choices=TimeSlot.choices,
        verbose_name=_("Time Slot"),
        help_text=_("Time slot for the reservation")
    )
    duration = models.PositiveIntegerField(
        default=30,
        verbose_name=_("Duration"),
        help_text=_("Total reservation duration in minutes")
    )

    class Meta:
        verbose_name = _("Reservation Schedule")
        verbose_name_plural = _("Reservation Schedules")
        ordering = ['date', 'time_slot']
        indexes = [
            models.Index(fields=['date', 'time_slot']),
            models.Index(fields=['operator']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'time_slot', 'operator'],
                name='unique_schedule_per_operator'
            ),
        ]

    def __str__(self) -> str:
        return f"{self.date} {self.get_period_display()} {self.get_time_slot_display()}"

    def clean(self) -> None:
        """Validate schedule fields."""
        if not self.date:
            raise ValidationError(_('Date cannot be empty'))
        if self.duration <= 0:
            raise ValidationError(_('Duration must be positive'))

    @classmethod
    def get_available_schedules(cls, date: str) -> List['ReservationSchedule']:
        """Retrieve available schedules for a specific date."""
        try:
            return list(cls.objects.filter(date=date))
        except Exception as e:
            logger.error(f"Error retrieving schedules for date {date}: {str(e)}")
            return []

class Reservation(BaseModel):
    """
    Model to store user reservations for laser treatments.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name=_("Reservation ID"),
        help_text=_("Unique identifier for the reservation")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reservations',
        verbose_name=_("User"),
        help_text=_("User who made the reservation")
    )
    schedule = models.ForeignKey(
        'ReservationSchedule',
        on_delete=models.PROTECT,
        related_name='reservations',
        verbose_name=_("Schedule"),
        help_text=_("Associated reservation schedule")
    )
    laser_area = models.ForeignKey(
        'LazerApp.LaserArea',
        on_delete=models.PROTECT,
        related_name='reservations',
        null=True,
        verbose_name=_("Laser Area"),
        help_text=_("Primary laser treatment area")
    )
    laser_area_schedules = models.ManyToManyField(
        'LazerApp.LaserAreaSchedule',
        related_name='reservations',
        verbose_name=_("Laser Area Schedules"),
        help_text=_("Scheduled laser areas for this reservation")
    )
    session_number = models.PositiveIntegerField(
        verbose_name=_("Session Number"),
        help_text=_("Session number for this reservation")
    )
    reservation_type = models.CharField(
        max_length=20,
        choices=ReservationType.choices,
        default=ReservationType.STANDARD,
        verbose_name=_("Reservation Type"),
        help_text=_("Type of reservation")
    )
    is_online = models.BooleanField(
        default=True,
        verbose_name=_("Is Online"),
        help_text=_("Indicates if reservation was made online")
    )
    is_charged = models.BooleanField(
        default=False,
        verbose_name=_("Is Charged"),
        help_text=_("Indicates if reservation has been charged")
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name=_("Is Paid"),
        help_text=_("Indicates if payment has been completed")
    )
    used_discount_code = models.BooleanField(
        default=False,
        verbose_name=_("Used Discount Code"),
        help_text=_("Indicates if a discount code was applied")
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        verbose_name=_("Total Price"),
        help_text=_("Total price before discounts")
    )
    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        verbose_name=_("Final Amount"),
        help_text=_("Final amount after discounts")
    )
    discount_code = models.ForeignKey(
        'DiscountCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservations',
        verbose_name=_("Discount Code"),
        help_text=_("Applied discount code, if any")
    )
    reservation_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Reservation Timestamp"),
        help_text=_("Timestamp when reservation was made")
    )
    request_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Request Timestamp"),
        help_text=_("Timestamp when reservation was requested")
    )

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        indexes = [
            models.Index(fields=['user', 'reservation_timestamp']),
            models.Index(fields=['is_paid', 'is_charged']),
        ]

    def __str__(self) -> str:
        return f"Reservation {self.id} - {self.user.username}"

    def clean(self) -> None:
        """Validate reservation fields."""
        if self.total_price < 0 or self.final_amount < 0:
            raise ValidationError(_('Price and amount cannot be negative'))
        if self.final_amount > self.total_price:
            raise ValidationError(_('Final amount cannot exceed total price'))
        if self.reservation_timestamp and self.request_timestamp and self.reservation_timestamp < self.request_timestamp:
            raise ValidationError(_('Reservation timestamp cannot be before request timestamp'))
        if self.used_discount_code and not self.discount_code:
            raise ValidationError(_('Discount code must be provided if used_discount_code is True'))

    @classmethod
    def get_unpaid_reservations(cls) -> List['Reservation']:
        """Retrieve all unpaid reservations."""
        try:
            return list(cls.objects.filter(is_paid=False))
        except Exception as e:
            logger.error(f"Error retrieving unpaid reservations: {str(e)}")
            return []

class PreReservation(BaseModel):
    """
    Model to store user's previous offline reservation information.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name=_("Pre-Reservation ID"),
        help_text=_("Unique identifier for the pre-reservation")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='pre_reservations',
        verbose_name=_("User"),
        help_text=_("User associated with this pre-reservation")
    )
    laser_area_schedule = models.ForeignKey(
        'LazerApp.LaserAreaSchedule',
        on_delete=models.PROTECT,
        related_name='pre_reservations',
        verbose_name=_("Laser Area Schedule"),
        help_text=_("Scheduled laser area for this pre-reservation")
    )
    session_count = models.PositiveIntegerField(
        verbose_name=_("Session Count"),
        help_text=_("Number of sessions for this pre-reservation")
    )
    last_session_date = models.DateField(
        verbose_name=_("Last Session Date"),
        help_text=_("Date of the last session")
    )

    class Meta:
        verbose_name = _("Pre-Reservation")
        verbose_name_plural = _("Pre-Reservations")
        indexes = [
            models.Index(fields=['user', 'last_session_date']),
        ]

    def __str__(self) -> str:
        return f"Pre-Reservation {self.id} - {self.user.username}"

    def clean(self) -> None:
        """Validate pre-reservation fields."""
        if not self.last_session_date:
            raise ValidationError(_('Last session date cannot be empty'))
        if self.session_count <= 0:
            raise ValidationError(_('Session count must be positive'))

    @classmethod
    def get_user_pre_reservations(cls, user_id: int) -> List['PreReservation']:
        """Retrieve all pre-reservations for a specific user."""
        try:
            return list(cls.objects.filter(user_id=user_id))
        except Exception as e:
            logger.error(f"Error retrieving pre-reservations for user {user_id}: {str(e)}")
            return []