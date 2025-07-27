from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.payment.serializers import PaymentSerializer, DiscountCodeSerializer

# PaymentAdminAPI methods Decorators
admin_create_payment_swagger = swagger_auto_schema(
    operation_summary='Create a New Payment (Admin)',
    operation_description=(
        'Allows administrators to create a new payment record. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.payment'],
    request_body=PaymentSerializer,
    responses={
        201: PaymentSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_payment_swagger = swagger_auto_schema(
    operation_summary='Retrieve Payment Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a payment by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.payment'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the payment to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: PaymentSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Payment does not exist.'
    }
)

admin_update_payment_swagger = swagger_auto_schema(
    operation_summary='Update Payment Details (Admin)',
    operation_description=(
        'Allows administrators to update a payment by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.payment'],
    request_body=PaymentSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the payment to update.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: PaymentSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Payment does not exist.'
    }
)

admin_list_payment_swagger = swagger_auto_schema(
    operation_summary='List All Payments (Admin)',
    operation_description=(
        'Lists all payments. '
        'Optional search functionality is available using the "search" query parameter to filter by username or paypal_transaction_id. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.payment'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter payments by username or PayPal transaction ID.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: PaymentSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_pending_payments_swagger = swagger_auto_schema(
    operation_summary='List Pending Payments (Admin)',
    operation_description=(
        'Allows administrators to retrieve a list of pending payments. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.payment'],
    responses={
        200: PaymentSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# PaymentCustomerAPIView Decorators
user_create_payment_swagger = swagger_auto_schema(
    operation_summary='Create a New Payment',
    operation_description=(
        'Allows customers to create a new payment record. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['payment.customer'],
    request_body=PaymentSerializer,
    responses={
        201: PaymentSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can create payments.'
    }
)

user_retrieve_payment_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Payment',
    operation_description=(
        'Allows customers to retrieve their own payment by its ID. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['payment.customer'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the payment to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: PaymentSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can access their own payments.',
        404: 'Not Found: Payment does not exist.'
    }
)

user_list_payment_swagger = swagger_auto_schema(
    operation_summary='List Own Payments',
    operation_description=(
        'Allows customers to list their own payments. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['payment.customer'],
    responses={
        200: PaymentSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can access their own payments.'
    }
)

# DiscountCodeAdminAPIView Decorators
admin_create_discount_code_swagger = swagger_auto_schema(
    operation_summary='Create a New Discount Code (Admin)',
    operation_description=(
        'Allows administrators to create a new discount code. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.payment.discount_code'],
    request_body=DiscountCodeSerializer,
    responses={
        201: DiscountCodeSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_discount_code_swagger = swagger_auto_schema(
    operation_summary='Retrieve Discount Code Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a discount code by its code. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.payment.discount_code'],
    manual_parameters=[
        openapi.Parameter('code', openapi.IN_PATH, description="The code of the discount code to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: DiscountCodeSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Discount code does not exist.'
    }
)

admin_update_discount_code_swagger = swagger_auto_schema(
    operation_summary='Update Discount Code Details (Admin)',
    operation_description=(
        'Allows administrators to update a discount code by its code. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.payment.discount_code'],
    request_body=DiscountCodeSerializer,
    manual_parameters=[
        openapi.Parameter('code', openapi.IN_PATH, description="The code of the discount code to update.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: DiscountCodeSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Discount code does not exist.'
    }
)

admin_list_discount_code_swagger = swagger_auto_schema(
    operation_summary='List All Discount Codes (Admin)',
    operation_description=(
        'Lists all discount codes. '
        'Optional search functionality is available using the "search" query parameter to filter by code. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.payment.discount_code'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter discount codes by code.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: DiscountCodeSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# DiscountCodeUserAPIView Decorators
user_list_discount_code_swagger = swagger_auto_schema(
    operation_summary='List Valid Discount Codes',
    operation_description=(
        'Allows authenticated users to list valid, unused discount codes. '
        'This operation requires JWT authentication.'
    ),
    tags=['payment.discount_code'],
    responses={
        200: DiscountCodeSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.'
    }
)

user_retrieve_discount_code_swagger = swagger_auto_schema(
    operation_summary='Retrieve Valid Discount Code',
    operation_description=(
        'Allows authenticated users to retrieve details of a valid discount code by its code. '
        'This operation requires JWT authentication.'
    ),
    tags=['payment.discount_code'],
    manual_parameters=[
        openapi.Parameter('code', openapi.IN_PATH, description="The code of the discount code to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: DiscountCodeSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        404: 'Not Found: Discount code does not exist or is not valid.'
    }
)

user_valid_codes_swagger = swagger_auto_schema(
    operation_summary='List Valid Discount Codes',
    operation_description=(
        'Allows authenticated users to retrieve a list of valid discount codes. '
        'This operation requires JWT authentication.'
    ),
    tags=['payment.discount_code'],
    responses={
        200: DiscountCodeSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.'
    }
)