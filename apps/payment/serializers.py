from typing import Dict, Any, List

from django.utils import timezone
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import logging
from .models import Payment, DiscountCode, PaymentStatus, PaymentType

from apps.core.models import CustomUser
from apps.reserve.models.reserve import Reservation

# Configure logging for better debugging and monitoring
logger = logging.getLogger(__name__)

class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model, handling payment transaction data.
    """
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True,
        required=True,
        help_text=_("ID of the associated user")
    )
    reservation_id = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all(),
        source='reservation',
        write_only=True,
        required=True,
        help_text=_("ID of the associated reservation")
    )
    user = serializers.StringRelatedField(read_only=True)
    reservation = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_id', 'reservation', 'reservation_id', 'amount',
            'status', 'payment_type', 'paypal_transaction_id', 'payment_timestamp',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'reservation']

    def validate_amount(self, value: float) -> float:
        """Validate the amount field."""
        if value < 0:
            logger.error(f"Negative amount provided: {value}")
            raise serializers.ValidationError(_('Payment amount cannot be negative'))
        return value

    def validate_status(self, value: str) -> str:
        """Validate the status field."""
        if value not in PaymentStatus.values:
            logger.error(f"Invalid payment status provided: {value}")
            raise serializers.ValidationError(_('Invalid payment status'))
        return value

    def validate_payment_type(self, value: str) -> str:
        """Validate the payment_type field."""
        if value not in PaymentType.values:
            logger.error(f"Invalid payment type provided: {value}")
            raise serializers.ValidationError(_('Invalid payment type'))
        return value

    def validate_paypal_transaction_id(self, value: str) -> str:
        """Validate the paypal_transaction_id field."""
        if value and len(value) > 100:
            logger.error(f"PayPal transaction ID exceeds 100 characters: {value}")
            raise serializers.ValidationError(_('PayPal transaction ID cannot exceed 100 characters'))
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the Payment instance."""
        try:
            instance = Payment(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in PaymentSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in PaymentSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> Payment:
        """Create a new Payment instance with validated data."""
        try:
            payment = Payment.objects.create(**validated_data)
            logger.info(f"Created payment: {payment.id} for user: {payment.user.username}")
            return payment
        except Exception as e:
            logger.error(f"Error creating payment: {str(e)}")
            raise serializers.ValidationError(_('Failed to create payment'))

    def update(self, instance: Payment, validated_data: Dict[str, Any]) -> Payment:
        """Update an existing Payment instance with validated data."""
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated payment: {instance.id} for user: {instance.user.username}")
            return instance
        except Exception as e:
            logger.error(f"Error updating payment {instance.id}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update payment'))

    def to_representation(self, instance: Payment) -> Dict[str, Any]:
        """Customize the representation to exclude user_id and reservation_id from the output."""
        representation = super().to_representation(instance)
        representation.pop('user_id', None)
        representation.pop('reservation_id', None)
        return representation

    @classmethod
    def get_pending_payments(cls) -> List[Dict[str, Any]]:
        """Retrieve serialized data for pending payments."""
        try:
            payments = Payment.get_pending_payments()
            return cls(many=True).to_representation(payments)
        except Exception as e:
            logger.error(f"Error retrieving pending payments: {str(e)}")
            return []

class DiscountCodeSerializer(serializers.ModelSerializer):
    """
    Serializer for the DiscountCode model, handling discount code data.
    """
    class Meta:
        model = DiscountCode
        fields = ['code', 'amount', 'is_used', 'valid_until', 'max_usage', 'usage_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'usage_count']

    def validate_code(self, value: str) -> str:
        """Validate the code field."""
        if not value.strip():
            logger.error("Discount code provided is empty")
            raise serializers.ValidationError(_('Discount code cannot be empty'))
        if len(value) > 10:
            logger.error(f"Discount code exceeds 10 characters: {value}")
            raise serializers.ValidationError(_('Discount code cannot exceed 10 characters'))
        return value

    def validate_amount(self, value: float) -> float:
        """Validate the amount field."""
        if value < 0:
            logger.error(f"Negative discount amount provided: {value}")
            raise serializers.ValidationError(_('Discount amount cannot be negative'))
        return value

    def validate_max_usage(self, value: int) -> int:
        """Validate the max_usage field."""
        if value <= 0:
            logger.error(f"Non-positive max usage provided: {value}")
            raise serializers.ValidationError(_('Maximum usage must be positive'))
        return value

    def validate_valid_until(self, value: Any) -> Any:
        """Validate the valid_until field."""
        if value and value < timezone.now():
            logger.error(f"Expired validity date provided: {value}")
            raise serializers.ValidationError(_('Discount code cannot have an expired validity date'))
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation for the DiscountCode instance."""
        try:
            instance = DiscountCode(**data)
            instance.clean()
            return data
        except ValidationError as e:
            logger.error(f"Validation error in DiscountCodeSerializer: {str(e)}")
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error in DiscountCodeSerializer validation: {str(e)}")
            raise serializers.ValidationError(_('An unexpected error occurred during validation'))

    def create(self, validated_data: Dict[str, Any]) -> DiscountCode:
        """Create a new DiscountCode instance with validated data."""
        try:
            discount_code = DiscountCode.objects.create(**validated_data)
            logger.info(f"Created discount code: {discount_code.code}")
            return discount_code
        except Exception as e:
            logger.error(f"Error creating discount code: {str(e)}")
            raise serializers.ValidationError(_('Failed to create discount code'))

    def update(self, instance: DiscountCode, validated_data: Dict[str, Any]) -> DiscountCode:
        """Update an existing DiscountCode instance with validated data."""
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info(f"Updated discount code: {instance.code}")
            return instance
        except Exception as e:
            logger.error(f"Error updating discount code {instance.code}: {str(e)}")
            raise serializers.ValidationError(_('Failed to update discount code'))

    @classmethod
    def get_valid_codes(cls) -> List[Dict[str, Any]]:
        """Retrieve serialized data for valid discount codes."""
        try:
            codes = DiscountCode.get_valid_codes()
            return cls(many=True).to_representation(codes)
        except Exception as e:
            logger.error(f"Error retrieving valid discount codes: {str(e)}")
            return []