from typing import Dict, Any, List
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import logging
from .models import LaserArea, LaserAreaSchedule

# Configure logging for better debugging and monitoring
logger = logging.getLogger(__name__)

class LaserAreaSerializer(serializers.ModelSerializer):
    """
    Serializer for the LaserArea model, handling laser treatment area data.
    """
    class Meta:
        model = LaserArea
        fields = ['name', 'current_price', 'deadline_reset', 'is_active', 'operate_time', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_name(self, value: str) -> str:
        """Validate the name field."""
        if not value.strip():
            logger.error("Laser area name provided is empty")
            raise serializers.ValidationError(_('Area name cannot be empty'))
        if len(value) > 50:
            logger.error(f"Laser area name exceeds 50 characters: {value}")
            raise serializers.ValidationError(_('Area name cannot exceed 50 characters'))
        return value

    def validate_current_price(self, value: float) -> float:
        """Validate the current_price field."""
        if value < 0:
            logger.error(f"Negative price provided: {value}")
            raise serializers.ValidationError(_('Price cannot be negative'))
        return value

    def validate_deadline_reset(self, value: int) -> int:
        """Validate the deadline_reset field."""
        if value < 0:
            logger.error(f"Negative deadline reset provided: {value}")
            raise serializers.ValidationError(_('Reset deadline cannot be negative'))
        return value

    def validate_operate_time(self, value: int) -> int:
        """Validate the operate_time field."""
        if value < 0:
            logger.error(f"Negative operate time provided: {value}")
            raise serializers.ValidationError(_('Operation time cannot be negative'))
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the LaserArea instance."""
        try:
            instance = LaserArea(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in LaserAreaSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in LaserAreaSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> LaserArea:
        """Create a new LaserArea instance with validated data."""
        try:
            laser_area = LaserArea.objects.create(**validated_data)
            logger.info(f"Created laser area: {laser_area.name} (ID: {laser_area.name})")
            return laser_area
        except Exception as e:
            logger.error(f"Error creating laser area: {str(e)}")
            raise serializers.ValidationError(_('Failed to create laser area'))

    def update(self, instance: LaserArea, validated_data: Dict[str, Any]) -> LaserArea:
        """Update an existing LaserArea instance with validated data."""
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated laser area: {instance.name} (ID: {instance.name})")
            return instance
        except Exception as e:
            logger.error(f"Error updating laser area {instance.name}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update laser area'))

class LaserAreaScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the LaserAreaSchedule model, handling scheduling data for laser areas.
    """
    laser_area_name = serializers.PrimaryKeyRelatedField(
        queryset=LaserArea.objects.all(),
        source='laser_area',
        write_only=True,
        required=True,
        help_text=_("Name of the associated laser area")
    )
    laser_area = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = LaserAreaSchedule
        fields = ['id', 'laser_area', 'laser_area_name', 'price', 'start_time', 'end_time', 'operate_time', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'laser_area']

    def validate_price(self, value: float) -> float:
        """Validate the price field."""
        if value < 0:
            logger.error(f"Negative price provided: {value}")
            raise serializers.ValidationError(_('Price cannot be negative'))
        return value

    def validate_operate_time(self, value: int) -> int:
        """Validate the operate_time field."""
        if value < 0:
            logger.error(f"Negative operate time provided: {value}")
            raise serializers.ValidationError(_('Operation time cannot be negative'))
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the LaserAreaSchedule instance."""
        try:
            instance = LaserAreaSchedule(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in LaserAreaScheduleSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in LaserAreaScheduleSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> LaserAreaSchedule:
        """Create a new LaserAreaSchedule instance with validated data."""
        try:
            schedule = LaserAreaSchedule.objects.create(**validated_data)
            logger.info(f"Created laser area schedule: {schedule.id} for area: {schedule.laser_area.name}")
            return schedule
        except Exception as e:
            logger.error(f"Error creating laser area schedule: {str(e)}")
            raise serializers.ValidationError(_('Failed to create laser area schedule'))

    def update(self, instance: LaserAreaSchedule, validated_data: Dict[str, Any]) -> LaserAreaSchedule:
        """Update an existing LaserAreaSchedule instance with validated data."""
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated laser area schedule: {instance.id} for area: {instance.laser_area.name}")
            return instance
        except Exception as e:
            logger.error(f"Error updating laser area schedule {instance.id}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update laser area schedule'))

    def to_representation(self, instance: LaserAreaSchedule) -> Dict[str, Any]:
        """Customize the representation to exclude laser_area_name from the output."""
        representation = super().to_representation(instance)
        representation.pop('laser_area_name', None)
        return representation

    @classmethod
    def get_active_schedules(cls) -> List[Dict[str, Any]]:
        """Retrieve serialized data for active laser area schedules."""
        try:
            schedules = LaserAreaSchedule.get_active_schedules()
            return cls(many=True).to_representation(schedules)
        except Exception as e:
            logger.error(f"Error retrieving active schedules: {str(e)}")
            return []