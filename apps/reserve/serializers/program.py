from typing import Dict, Any, List
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import logging

from apps.core.models import CustomUser
from apps.reserve.models.program import OperatorShift, CancellationPeriod, DayPeriod

# Configure logging for better debugging and monitoring
logger = logging.getLogger(__name__)

class OperatorShiftSerializer(serializers.ModelSerializer):
    """
    Serializer for the OperatorShift model, handling operator shift assignments.
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
        model = OperatorShift
        fields = ['id', 'operator', 'operator_id', 'operator_name', 'shift_date', 'period', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'operator']

    def validate_operator_name(self, value: str) -> str:
        """Validate the operator_name field."""
        if value and len(value) > 50:
            logger.error(f"Operator name exceeds 50 characters: {value}")
            raise serializers.ValidationError(_('Operator name cannot exceed 50 characters'))
        return value

    def validate_period(self, value: str) -> str:
        """Validate the period field."""
        if value not in DayPeriod.values:
            logger.error(f"Invalid period provided: {value}")
            raise serializers.ValidationError(_('Invalid period'))
        return value

    def validate_shift_date(self, value: Any) -> Any:
        """Validate the shift_date field."""
        if not value:
            logger.error("Shift date provided is empty")
            raise serializers.ValidationError(_('Shift date cannot be empty'))
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the OperatorShift instance."""
        try:
            instance = OperatorShift(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in OperatorShiftSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in OperatorShiftSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> OperatorShift:
        """Create a new OperatorShift instance with validated data."""
        try:
            shift = OperatorShift.objects.create(**validated_data)
            logger.info(f"Created operator shift: {shift.id} for operator: {shift.operator.username}")
            return shift
        except Exception as e:
            logger.error(f"Error creating operator shift: {str(e)}")
            raise serializers.ValidationError(_('Failed to create operator shift'))

    def update(self, instance: OperatorShift, validated_data: Dict[str, Any]) -> OperatorShift:
        """Update an existing OperatorShift instance with validated data."""
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated operator shift: {instance.id} for operator: {instance.operator.username}")
            return instance
        except Exception as e:
            logger.error(f"Error updating operator shift {instance.id}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update operator shift'))

    def to_representation(self, instance: OperatorShift) -> Dict[str, Any]:
        """Customize the representation to exclude operator_id from the output."""
        representation = super().to_representation(instance)
        representation.pop('operator_id', None)
        return representation

    @classmethod
    def get_shifts_by_date(cls, shift_date: str) -> List[Dict[str, Any]]:
        """Retrieve serialized data for shifts on a specific date."""
        try:
            shifts = OperatorShift.get_shifts_by_date(shift_date)
            return cls(many=True).to_representation(shifts)
        except Exception as e:
            logger.error(f"Error retrieving shifts for date {shift_date}: {str(e)}")
            return []

class CancellationPeriodSerializer(serializers.ModelSerializer):
    """
    Serializer for the CancellationPeriod model, handling cancellation period data.
    """
    class Meta:
        model = CancellationPeriod
        fields = ['id', 'start_time', 'end_time', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the CancellationPeriod instance."""
        try:
            instance = CancellationPeriod(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in CancellationPeriodSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in CancellationPeriodSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> CancellationPeriod:
        """Create a new CancellationPeriod instance with validated data."""
        try:
            cancellation = CancellationPeriod.objects.create(**validated_data)
            logger.info(f"Created cancellation period: {cancellation.id}")
            return cancellation
        except Exception as e:
            logger.error(f"Error creating cancellation period: {str(e)}")
            raise serializers.ValidationError(_('Failed to create cancellation period'))

    def update(self, instance: CancellationPeriod, validated_data: Dict[str, Any]) -> CancellationPeriod:
        """Update an existing CancellationPeriod instance with validated data."""
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated cancellation period: {instance.id}")
            return instance
        except Exception as e:
            logger.error(f"Error updating cancellation period {instance.id}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update cancellation period'))

    @classmethod
    def get_active_cancellations(cls) -> List[Dict[str, Any]]:
        """Retrieve serialized data for active cancellation periods."""
        try:
            cancellations = CancellationPeriod.get_active_cancellations()
            return cls(many=True).to_representation(cancellations)
        except Exception as e:
            logger.error(f"Error retrieving active cancellation periods: {str(e)}")
            return []