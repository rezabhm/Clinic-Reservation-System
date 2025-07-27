from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging
from uuid import uuid4
from typing import List
from django.conf import settings

from apps.core.models import BaseModel

# Configure logging for better debugging and monitoring
logger = logging.getLogger(__name__)


class DayPeriod(models.TextChoices):
    MORNING = 'MORNING', _('Morning')
    AFTERNOON = 'AFTERNOON', _('Afternoon')

class OperatorShift(BaseModel):
    """
    Model to store operator shift assignments for reservation scheduling.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name=_("Shift ID"),
        help_text=_("Unique identifier for the operator shift")
    )
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='shifts',
        verbose_name=_("Operator"),
        help_text=_("User assigned as the operator for this shift")
    )
    operator_name = models.CharField(
        max_length=50,
        verbose_name=_("Operator Name"),
        help_text=_("Display name of the operator (max 50 characters)"),
        blank=True
    )
    shift_date = models.DateField(
        verbose_name=_("Shift Date"),
        help_text=_("Date of the operator's shift")
    )
    period = models.CharField(
        max_length=20,
        choices=DayPeriod.choices,
        default=DayPeriod.MORNING,
        verbose_name=_("Shift Period"),
        help_text=_("Period of the day for the shift (morning or afternoon)")
    )

    class Meta:
        verbose_name = _("Operator Shift")
        verbose_name_plural = _("Operator Shifts")
        indexes = [
            models.Index(fields=['operator', 'shift_date']),
            models.Index(fields=['period']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['operator', 'shift_date', 'period'],
                name='unique_shift_per_operator_date_period'
            ),
        ]

    def __str__(self) -> str:
        return f"{self.operator_name or self.operator.username} - {self.shift_date} ({self.get_period_display()})"

    def clean(self) -> None:
        """Validate operator shift fields."""
        if not self.operator:
            raise ValidationError(_('Operator is required'))
        if not self.operator_name:
            self.operator_name = self.operator.username
        if not self.shift_date:
            raise ValidationError(_('Shift date cannot be empty'))
        if self.period not in DayPeriod.values:
            raise ValidationError(_('Invalid shift period'))

    def save(self, *args, **kwargs) -> None:
        """Override save to ensure operator_name is set."""
        if not self.operator_name and self.operator:
            self.operator_name = self.operator.username
        super().save(*args, **kwargs)

    @classmethod
    def get_shifts_by_date(cls, shift_date: str) -> List['OperatorShift']:
        """Retrieve all shifts for a specific date."""
        try:
            return list(cls.objects.filter(shift_date=shift_date))
        except Exception as e:
            logger.error(f"Error retrieving shifts for date {shift_date}: {str(e)}")
            return []

    @classmethod
    def get_active_shifts(cls, user) -> List['OperatorShift']:
        """
        Retrieve all active (today or future) shifts for a given operator (user).
        """
        try:
            today = timezone.localdate()
            return list(cls.objects.filter(operator=user, shift_date__gte=today))
        except Exception as e:
            logger.error(f"Error retrieving active shifts for operator {user}: {str(e)}")
            return []


class CancellationPeriod(BaseModel):
    """
    Model to store time periods when reservations are cancelled by admin.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name=_("Cancellation ID"),
        help_text=_("Unique identifier for the cancellation period")
    )
    start_time = models.DateTimeField(
        verbose_name=_("Start Time"),
        help_text=_("Start of the cancellation period")
    )
    end_time = models.DateTimeField(
        verbose_name=_("End Time"),
        help_text=_("End of the cancellation period")
    )

    class Meta:
        verbose_name = _("Cancellation Period")
        verbose_name_plural = _("Cancellation Periods")
        indexes = [
            models.Index(fields=['start_time', 'end_time']),
        ]

    def __str__(self) -> str:
        return f"Cancellation {self.id} - {self.start_time} to {self.end_time}"

    def clean(self) -> None:
        """Validate cancellation period fields."""
        if not self.start_time or not self.end_time:
            raise ValidationError(_('Start and end times are required'))
        if self.end_time <= self.start_time:
            raise ValidationError(_('End time must be after start time'))
        if self.start_time < timezone.now():
            raise ValidationError(_('Cancellation period cannot start in the past'))

    @classmethod
    def get_active_cancellations(cls) -> List['CancellationPeriod']:
        """Retrieve all active cancellation periods."""
        try:
            return list(cls.objects.filter(end_time__gte=timezone.now()))
        except Exception as e:
            logger.error(f"Error retrieving active cancellation periods: {str(e)}")
            return []