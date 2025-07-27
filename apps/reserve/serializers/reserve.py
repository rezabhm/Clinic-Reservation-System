from typing import Dict, Any, List
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import logging

from apps.core.models import CustomUser
from apps.payment.models import DiscountCode
from apps.reserve.models.reserve import (ReservationSchedule, Reservation, PreReservation, TimeSlot, DayPeriod,
                                         ReservationType)
from apps.lazer_area.models import LaserArea, LaserAreaSchedule

# Configure logging for better debugging and monitoring
logger = logging.getLogger(__name__)

class ReservationScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the ReservationSchedule model, handling reservation scheduling data.
    """
    operator_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='operator',
        write_only=True,
        required=True,
        help_text=_("ID of the associated operator")
    )
    operator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ReservationSchedule
        fields = ['id', 'operator', 'operator_id', 'date', 'period', 'time_slot', 'duration', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'operator']

    def validate_period(self, value: str) -> str:
        """Validate the period field."""
        if value not in DayPeriod.values:
            logger.error(f"Invalid period provided: {value}")
            raise serializers.ValidationError(_('Invalid period'))
        return value

    def validate_time_slot(self, value: str) -> str:
        """Validate the time_slot field."""
        if value not in TimeSlot.values:
            logger.error(f"Invalid time slot provided: {value}")
            raise serializers.ValidationError(_('Invalid time slot'))
        return value

    def validate_duration(self, value: int) -> int:
        """Validate the duration field."""
        if value <= 0:
            logger.error(f"Non-positive duration provided: {value}")
            raise serializers.ValidationError(_('Duration must be positive'))
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the ReservationSchedule instance."""
        try:
            instance = ReservationSchedule(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in ReservationScheduleSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in ReservationScheduleSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> ReservationSchedule:
        """Create a new ReservationSchedule instance with validated data."""
        try:
            schedule = ReservationSchedule.objects.create(**validated_data)
            logger.info(f"Created reservation schedule: {schedule.id} for operator: {schedule.operator.username}")
            return schedule
        except Exception as e:
            logger.error(f"Error creating reservation schedule: {str(e)}")
            raise serializers.ValidationError(_('Failed to create reservation schedule'))

    def update(self, instance: ReservationSchedule, validated_data: Dict[str, Any]) -> ReservationSchedule:
        """Update an existing ReservationSchedule instance with validated data."""
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated reservation schedule: {instance.id} for operator: {instance.operator.username}")
            return instance
        except Exception as e:
            logger.error(f"Error updating reservation schedule {instance.id}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update reservation schedule'))

    def to_representation(self, instance: ReservationSchedule) -> Dict[str, Any]:
        """Customize the representation to exclude operator_id from the output."""
        representation = super().to_representation(instance)
        representation.pop('operator_id', None)
        return representation

    @classmethod
    def get_available_schedules(cls, date: str) -> List[Dict[str, Any]]:
        """Retrieve serialized data for available schedules on a specific date."""
        try:
            schedules = ReservationSchedule.get_available_schedules(date)
            return cls(many=True).to_representation(schedules)
        except Exception as e:
            logger.error(f"Error retrieving available schedules: {str(e)}")
            return []

class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Reservation model, handling reservation data.
    """
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True,
        required=True,
        help_text=_("ID of the associated user")
    )
    schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=ReservationSchedule.objects.all(),
        source='schedule',
        write_only=True,
        required=True,
        help_text=_("ID of the associated schedule")
    )
    laser_area_id = serializers.PrimaryKeyRelatedField(
        queryset=LaserArea.objects.all(),
        source='laser_area',
        write_only=True,
        required=False,
        help_text=_("ID of the associated laser area")
    )
    laser_area_schedules_ids = serializers.PrimaryKeyRelatedField(
        queryset=LaserAreaSchedule.objects.all(),
        source='laser_area_schedules',
        many=True,
        write_only=True,
        required=False,
        help_text=_("IDs of the associated laser area schedules")
    )
    discount_code_id = serializers.PrimaryKeyRelatedField(
        queryset=DiscountCode.objects.all(),
        source='discount_code',
        write_only=True,
        required=False,
        help_text=_("ID of the associated discount code")
    )
    user = serializers.StringRelatedField(read_only=True)
    schedule = serializers.StringRelatedField(read_only=True)
    laser_area = serializers.StringRelatedField(read_only=True)
    laser_area_schedules = serializers.StringRelatedField(many=True, read_only=True)
    discount_code = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'user_id', 'schedule', 'schedule_id', 'laser_area', 'laser_area_id',
            'laser_area_schedules', 'laser_area_schedules_ids', 'session_number', 'reservation_type',
            'is_online', 'is_charged', 'is_paid', 'used_discount_code', 'total_price',
            'final_amount', 'discount_code', 'discount_code_id', 'reservation_timestamp',
            'request_timestamp', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'schedule', 'laser_area', 'laser_area_schedules', 'discount_code']

    def validate_session_number(self, value: int) -> int:
        """Validate the session_number field."""
        if value <= 0:
            logger.error(f"Non-positive session number provided: {value}")
            raise serializers.ValidationError(_('Session number must be positive'))
        return value

    def validate_reservation_type(self, value: str) -> str:
        """Validate the reservation_type field."""
        if value not in ReservationType.values:
            logger.error(f"Invalid reservation type provided: {value}")
            raise serializers.ValidationError(_('Invalid reservation type'))
        return value

    def validate_total_price(self, value: float) -> float:
        """Validate the total_price field."""
        if value < 0:
            logger.error(f"Negative total price provided: {value}")
            raise serializers.ValidationError(_('Total price cannot be negative'))
        return value

    def validate_final_amount(self, value: float) -> float:
        """Validate the final_amount field."""
        if value < 0:
            logger.error(f"Negative final amount provided: {value}")
            raise serializers.ValidationError(_('Final amount cannot be negative'))
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the Reservation instance."""
        try:
            instance = Reservation(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in ReservationSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in ReservationSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> Reservation:
        """Create a new Reservation instance with validated data."""
        try:
            laser_area_schedules = validated_data.pop('laser_area_schedules', [])
            reservation = Reservation.objects.create(**validated_data)
            if laser_area_schedules:
                reservation.laser_area_schedules.set(laser_area_schedules)
            logger.info(f"Created reservation: {reservation.id} for user: {reservation.user.username}")
            return reservation
        except Exception as e:
            logger.error(f"Error creating reservation: {str(e)}")
            raise serializers.ValidationError(_('Failed to create reservation'))

    def update(self, instance: Reservation, validated_data: Dict[str, Any]) -> Reservation:
        """Update an existing Reservation instance with validated data."""
        try:
            laser_area_schedules = validated_data.pop('laser_area_schedules', None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            if laser_area_schedules is not None:
                instance.laser_area_schedules.set(laser_area_schedules)
            instance.save()
            logger.info(f"Updated reservation: {instance.id} for user: {instance.user.username}")
            return instance
        except Exception as e:
            logger.error(f"Error updating reservation {instance.id}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update reservation'))

    def to_representation(self, instance: Reservation) -> Dict[str, Any]:
        """Customize the representation to exclude write-only fields from the output."""
        representation = super().to_representation(instance)
        representation.pop('user_id', None)
        representation.pop('schedule_id', None)
        representation.pop('laser_area_id', None)
        representation.pop('laser_area_schedules_ids', None)
        representation.pop('discount_code_id', None)
        return representation

    @classmethod
    def get_unpaid_reservations(cls) -> List[Dict[str, Any]]:
        """Retrieve serialized data for unpaid reservations."""
        try:
            reservations = Reservation.get_unpaid_reservations()
            return cls(many=True).to_representation(reservations)
        except Exception as e:
            logger.error(f"Error retrieving unpaid reservations: {str(e)}")
            return []

class PreReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for the PreReservation model, handling pre-reservation data.
    """
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True,
        required=True,
        help_text=_("ID of the associated user")
    )
    laser_area_schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=LaserAreaSchedule.objects.all(),
        source='laser_area_schedule',
        write_only=True,
        required=True,
        help_text=_("ID of the associated laser area schedule")
    )
    user = serializers.StringRelatedField(read_only=True)
    laser_area_schedule = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PreReservation
        fields = [
            'id', 'user', 'user_id', 'laser_area_schedule', 'laser_area_schedule_id',
            'session_count', 'last_session_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'laser_area_schedule']

    def validate_session_count(self, value: int) -> int:
        """Validate the session_count field."""
        if value <= 0:
            logger.error(f"Non-positive session count provided: {value}")
            raise serializers.ValidationError(_('Session count must be positive'))
        return value

    def validate_last_session_date(self, value: Any) -> Any:
        """Validate the last_session_date field."""
        if not value:
            logger.error("Last session date provided is empty")
            raise serializers.ValidationError(_('Last session date cannot be empty'))
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the PreReservation instance."""
        try:
            instance = PreReservation(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in PreReservationSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in PreReservationSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> PreReservation:
        """Create a new PreReservation instance with validated data."""
        try:
            pre_reservation = PreReservation.objects.create(**validated_data)
            logger.info(f"Created pre-reservation: {pre_reservation.id} for user: {pre_reservation.user.username}")
            return pre_reservation
        except Exception as e:
            logger.error(f"Error creating pre-reservation: {str(e)}")
            raise serializers.ValidationError(_('Failed to create pre-reservation'))

    def update(self, instance: PreReservation, validated_data: Dict[str, Any]) -> PreReservation:
        """Update an existing PreReservation instance with validated data."""
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated pre-reservation: {instance.id} for user: {instance.user.username}")
            return instance
        except Exception as e:
            logger.error(f"Error updating pre-reservation {instance.id}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update pre-reservation'))

    def to_representation(self, instance: PreReservation) -> Dict[str, Any]:
        """Customize the representation to exclude write-only fields from the output."""
        representation = super().to_representation(instance)
        representation.pop('user_id', None)
        representation.pop('laser_area_schedule_id', None)
        return representation