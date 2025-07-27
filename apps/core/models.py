from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging
from uuid import uuid4
from typing import List

# Configure logging for better debugging and monitoring
logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    """
    Abstract base model providing common timestamp fields.
    """
    created_at = models.DateTimeField(verbose_name=_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        """
        Override save method to include validation and logging.
        """
        try:
            self.full_clean()
            self.updated_at = timezone.now()
            super().save(*args, **kwargs)
            logger.info(f"Successfully saved {self.__class__.__name__} with ID: {self.id}")
        except ValidationError as e:
            logger.error(f"Validation error saving {self.__class__.__name__}: {str(e)}")
            raise


class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', _('Administrator')
    CUSTOMER = 'CUSTOMER', _('Customer')
    STAFF = 'STAFF', _('Staff')


class CustomUser(AbstractUser, BaseModel):
    """
    Custom user model extending AbstractUser with role-based access control.
    """
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
        verbose_name=_('Role'),
        help_text=_('Defines the user role and access level')
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        indexes = [
            models.Index(fields=['role', 'username', 'email', 'first_name', 'last_name']),
        ]

    def __str__(self) -> str:
        return self.username

    def clean(self) -> None:
        """Validate user role."""
        if self.role not in UserRole.values:
            raise ValidationError(_('Invalid user role selected'))

    def save(self, *args, **kwargs) -> None:
        """Override save with validation and logging."""
        try:
            self.full_clean()
            super().save(*args, **kwargs)
            logger.info(f"Successfully saved User: {self.username} (ID: {self.id})")
        except ValidationError as e:
            logger.error(f"Validation error saving User: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error saving User: {str(e)}")
            raise


class StaffAttendance(BaseModel):
    """
    Model to track staff entry and exit times with validation and logging.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name=_('User'),
        help_text=_('Associated user for this attendance record')
    )
    entry_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Entry Timestamp'),
        help_text=_('Timestamp of staff entry')
    )
    exit_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Exit Timestamp'),
        help_text=_('Timestamp of staff exit')
    )
    has_exited = models.BooleanField(
        default=False,
        verbose_name=_('Has Exited'),
        help_text=_('Indicates if the user has exited')
    )

    class Meta:
        verbose_name = _('Staff Attendance')
        verbose_name_plural = _('Staff Attendances')
        indexes = [
            models.Index(fields=['user', 'entry_timestamp']),
            models.Index(fields=['has_exited']),
        ]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.entry_timestamp or 'No Entry'}"

    def clean(self) -> None:
        """Validate attendance timestamps."""
        if self.exit_timestamp and self.entry_timestamp and self.exit_timestamp <= self.entry_timestamp:
            raise ValidationError(_('Exit timestamp must be after entry timestamp'))

    @classmethod
    def get_active_attendances(cls) -> List['StaffAttendance']:
        """Retrieve all active attendance records."""
        try:
            return list(cls.objects.filter(has_exited=False))
        except Exception as e:
            logger.error(f"Error retrieving active attendances: {str(e)}")
            return []


class CustomerProfile(BaseModel):
    """
    Model to store customer-specific information with validation and logging.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User'),
        help_text=_('Associated user for this profile')
    )
    national_id = models.CharField(
        max_length=15,
        unique=True,
        verbose_name=_('National ID'),
        help_text=_('Unique national identification number')
    )
    address = models.TextField(
        verbose_name=_('Address'),
        help_text=_('Customer residential address')
    )
    house_number = models.CharField(
        max_length=15,
        verbose_name=_('House Number'),
        help_text=_('House or apartment number')
    )
    has_medical_history = models.BooleanField(
        default=False,
        verbose_name=_('Has Medical History'),
        help_text=_('Indicates if customer has medical history')
    )
    has_drug_history = models.BooleanField(
        default=False,
        verbose_name=_('Has Drug History'),
        help_text=_('Indicates if customer has drug usage history')
    )
    primary_physician = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Primary Physician'),
        help_text=_('Name of the primary physician')
    )
    is_premium = models.BooleanField(
        default=False,
        verbose_name=_('Is Premium'),
        help_text=_('Indicates if customer has premium status')
    )
    offline_appointments = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Offline Appointments'),
        help_text=_('Number of offline appointments')
    )
    last_visit_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Last Visit Date'),
        help_text=_('Date of the last visit')
    )

    class Meta:
        verbose_name = _('Customer Profile')
        verbose_name_plural = _('Customer Profiles')
        indexes = [
            models.Index(fields=['national_id']),
            models.Index(fields=['user']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['national_id'], name='unique_national_id'),
        ]

    def __str__(self) -> str:
        return f"{self.national_id} - {self.user.username}"

    def clean(self) -> None:
        """Validate customer profile fields."""
        if not self.national_id.strip():
            raise ValidationError(_('National ID cannot be empty'))
        if self.offline_appointments < 0:
            raise ValidationError(_('Offline appointments cannot be negative'))


class Comments(BaseModel):
    """
    Model to store user Comments with validation and logging.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='Comments',
        verbose_name=_('User'),
        help_text=_('User who submitted the Comments')
    )
    message = models.TextField(
        verbose_name=_('Comments Message'),
        help_text=_('Content of the Comments')
    )
    is_reviewed = models.BooleanField(
        default=False,
        verbose_name=_('Is Reviewed'),
        help_text=_('Indicates if Comments has been reviewed')
    )

    class Meta:
        verbose_name = _('Comments')
        verbose_name_plural = _('Comments')
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['is_reviewed']),
        ]

    def __str__(self) -> str:
        return f"Comments from {self.user.username} at {self.created_at}"

    def clean(self) -> None:
        """Validate Comments message."""
        if not self.message.strip():
            raise ValidationError(_('Comments message cannot be empty'))

    @classmethod
    def get_unreviewed_Comments(cls) -> List['Comments']:
        """Retrieve all unreviewed Comments."""
        try:
            return list(cls.objects.filter(is_reviewed=False))
        except Exception as e:
            logger.error(f"Error retrieving unreviewed Comments: {str(e)}")
            return []