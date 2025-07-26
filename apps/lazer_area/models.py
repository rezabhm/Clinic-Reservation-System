from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging
from uuid import uuid4
from typing import List

from apps.core.models import BaseModel

# Configure logging for better debugging and monitoring
logger = logging.getLogger(__name__)


class LaserArea(BaseModel):
    """
    Model to store laser treatment area details with pricing and operational settings.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Area Name"),
        help_text=_("Name of the laser treatment area (max 50 characters)")
    )
    current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Current Price"),
        help_text=_("Current price for the laser treatment area")
    )
    deadline_reset = models.PositiveIntegerField(
        default=30,
        verbose_name=_("Session Reset Deadline"),
        help_text=_("Number of days before resetting laser operation session")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Indicates if the laser area is currently active")
    )
    operate_time = models.PositiveIntegerField(
        default=5,
        verbose_name=_("Operation Time"),
        help_text=_("Duration of laser operation in minutes")
    )

    class Meta:
        verbose_name = _("Laser Area")
        verbose_name_plural = _("Laser Areas")
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_laser_area_name'),
        ]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        """Validate laser area fields."""
        if not self.name.strip():
            raise ValidationError(_('Area name cannot be empty'))
        if self.current_price < 0:
            raise ValidationError(_('Price cannot be negative'))
        if self.deadline_reset < 0:
            raise ValidationError(_('Reset deadline cannot be negative'))
        if self.operate_time < 0:
            raise ValidationError(_('Operation time cannot be negative'))

class LaserAreaSchedule(BaseModel):
    """
    Model to store scheduling and pricing details for laser treatment areas.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    laser_area = models.ForeignKey(
        LaserArea,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name=_("Laser Area"),
        help_text=_("Associated laser treatment area")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Price"),
        help_text=_("Price for the scheduled session")
    )
    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Start Time"),
        help_text=_("Start time of the laser session")
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("End Time"),
        help_text=_("End time of the laser session")
    )
    operate_time = models.PositiveIntegerField(
        default=5,
        verbose_name=_("Operation Time"),
        help_text=_("Duration of laser operation in minutes")
    )

    class Meta:
        verbose_name = _("Laser Area Schedule")
        verbose_name_plural = _("Laser Area Schedules")
        indexes = [
            models.Index(fields=['laser_area', 'start_time']),
        ]

    def __str__(self) -> str:
        return f"{self.laser_area.name} - {self.start_time or 'No Start Time'}"

    def clean(self) -> None:
        """Validate schedule fields."""
        if self.price < 0:
            raise ValidationError(_('Price cannot be negative'))
        if self.operate_time < 0:
            raise ValidationError(_('Operation time cannot be negative'))
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError(_('End time must be after start time'))

    @classmethod
    def get_active_schedules(cls) -> List['LaserAreaSchedule']:
        """Retrieve all active schedules with non-null start times."""
        try:
            return list(cls.objects.filter(start_time__isnull=False))
        except Exception as e:
            logger.error(f"Error retrieving active schedules: {str(e)}")
            return []