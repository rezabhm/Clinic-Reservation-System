from typing import Dict, Any, List
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import logging
from apps.core.models import CustomUser, StaffAttendance, CustomerProfile, Comments, UserRole

# Configure logging for better debugging and monitoring
logger = logging.getLogger(__name__)


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model, handling user data and role assignment.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_role(self, value: str) -> str:
        """Validate the role field."""
        if value not in UserRole.values:
            logger.error(f"Invalid role provided: {value}")
            raise serializers.ValidationError(_('Invalid user role'))
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the CustomUser instance."""
        try:
            instance = CustomUser(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in CustomUserSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in CustomUserSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> CustomUser:
        """Create a new CustomUser instance with validated data."""
        try:
            user = CustomUser.objects.create_user(**validated_data)
            logger.info(f"Created user: {user.username} (ID: {user.id})")
            return user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise serializers.ValidationError(_('Failed to create user'))

    def update(self, instance: CustomUser, validated_data: Dict[str, Any]) -> CustomUser:
        """Update an existing CustomUser instance with validated data."""
        try:
            for attr, value in validated_data.items():
                if attr == 'password':
                    instance.set_password(value)
                else:
                    setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated user: {instance.username} (ID: {instance.id})")
            return instance
        except Exception as e:
            logger.error(f"Error updating user {instance.username}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update user'))

class StaffAttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the StaffAttendance model, handling attendance records.
    """
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True,
        required=True,
        help_text=_("ID of the associated user")
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StaffAttendance
        fields = ['id', 'user', 'user_id', 'entry_timestamp', 'exit_timestamp', 'has_exited', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the StaffAttendance instance."""
        try:
            instance = StaffAttendance(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in StaffAttendanceSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in StaffAttendanceSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> StaffAttendance:
        """Create a new StaffAttendance instance with validated data."""
        try:
            attendance = StaffAttendance.objects.create(**validated_data)
            logger.info(f"Created attendance: {attendance.id} for user: {attendance.user.username}")
            return attendance
        except Exception as e:
            logger.error(f"Error creating attendance: {str(e)}")
            raise serializers.ValidationError(_('Failed to create attendance'))

    def update(self, instance: StaffAttendance, validated_data: Dict[str, Any]) -> StaffAttendance:
        """Update an existing StaffAttendance instance with validated data."""
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated attendance: {instance.id} for user: {instance.user.username}")
            return instance
        except Exception as e:
            logger.error(f"Error updating attendance {instance.id}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update attendance'))

    def to_representation(self, instance: StaffAttendance) -> Dict[str, Any]:
        """Customize the representation to exclude user_id from the output."""
        representation = super().to_representation(instance)
        representation.pop('user_id', None)
        return representation

class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomerProfile model, handling customer-specific data.
    """
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True,
        required=True,
        help_text=_("ID of the associated user")
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = [
            'id', 'user', 'user_id', 'national_id', 'address', 'house_number',
            'has_medical_history', 'has_drug_history', 'primary_physician',
            'is_premium', 'offline_appointments', 'last_visit_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def validate_national_id(self, value: str) -> str:
        """Validate the national_id field."""
        if not value.strip():
            logger.error("National ID provided is empty")
            raise serializers.ValidationError(_('National ID cannot be empty'))
        if len(value) > 15:
            logger.error(f"National ID exceeds 15 characters: {value}")
            raise serializers.ValidationError(_('National ID cannot exceed 15 characters'))
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the CustomerProfile instance."""
        try:
            instance = CustomerProfile(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in CustomerProfileSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in CustomerProfileSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> CustomerProfile:
        """Create a new CustomerProfile instance with validated data."""
        try:
            profile = CustomerProfile.objects.create(**validated_data)
            logger.info(f"Created customer profile: {profile.national_id} (ID: {profile.id})")
            return profile
        except Exception as e:
            logger.error(f"Error creating customer profile: {str(e)}")
            raise serializers.ValidationError(_('Failed to create customer profile'))

    def update(self, instance: CustomerProfile, validated_data: Dict[str, Any]) -> CustomerProfile:
        """Update an existing CustomerProfile instance with validated data."""
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated customer profile: {instance.national_id} (ID: {instance.id})")
            return instance
        except Exception as e:
            logger.error(f"Error updating customer profile {instance.national_id}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update customer profile'))

    def to_representation(self, instance: CustomerProfile) -> Dict[str, Any]:
        """Customize the representation to exclude user_id from the output."""
        representation = super().to_representation(instance)
        representation.pop('user_id', None)
        return representation


class CommentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model, handling user comments data.
    """
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True,
        required=True,
        help_text=_("ID of the associated user")
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'user', 'user_id', 'message', 'is_reviewed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def validate_message(self, value: str) -> str:
        """Validate the message field."""
        if not value.strip():
            logger.error("Comments message provided is empty")
            raise serializers.ValidationError(_('Comments message cannot be empty'))
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the Feedback instance."""
        try:
            instance = Comments(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in CommentsSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in CommentsSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> Comments:
        """Create a new comment instance with validated data."""
        try:
            comments = Comments.objects.create(**validated_data)
            logger.info(f"Created Comments: {comments.id} for user: {comments.user.username}")
            return comments
        except Exception as e:
            logger.error(f"Error creating Comments: {str(e)}")
            raise serializers.ValidationError(_('Failed to create Comments'))

    def update(self, instance: Comments, validated_data: Dict[str, Any]) -> Comments:
        """Update an existing Comments instance with validated data."""
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated Comments: {instance.id} for user: {instance.user.username}")
            return instance
        except Exception as e:
            logger.error(f"Error updating Comments {instance.id}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update Comments'))

    def to_representation(self, instance: Comments) -> Dict[str, Any]:
        """Customize the representation to exclude user_id from the output."""
        representation = super().to_representation(instance)
        representation.pop('user_id', None)
        return representation

    @classmethod
    def get_unreviewed_feedback(cls) -> List[Dict[str, Any]]:
        """Retrieve serialized data for unreviewed feedback."""
        try:
            feedback = Comments.get_unreviewed_feedback()
            return cls(many=True).to_representation(feedback)
        except Exception as e:
            logger.error(f"Error retrieving unreviewed feedback: {str(e)}")
            return []