from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.reserve.serializers.program import OperatorShiftSerializer, CancellationPeriodSerializer

# OperatorShiftAdminAPIView Decorators
admin_create_shift_swagger = swagger_auto_schema(
    operation_summary='Create a New Operator Shift (Admin)',
    operation_description=(
        'Allows administrators to create a new operator shift. '
        'The request must include operator, date, start_time, and end_time. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.operatorprogram.shift'],
    request_body=OperatorShiftSerializer,
    responses={
        201: OperatorShiftSerializer,
        400: 'Invalid input data (e.g., invalid date or time).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_shift_swagger = swagger_auto_schema(
    operation_summary='Retrieve Operator Shift Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a specific operator shift by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.operatorprogram.shift'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the shift to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: OperatorShiftSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Shift with the specified ID does not exist.'
    }
)

admin_update_shift_swagger = swagger_auto_schema(
    operation_summary='Update Operator Shift Details (Admin)',
    operation_description=(
        'Allows administrators to fully update an operator shift identified by its ID. '
        'The request body must include all required fields even if some remain unchanged. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.operatorprogram.shift'],
    request_body=OperatorShiftSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the shift to update.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: OperatorShiftSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Shift with the specified ID does not exist.'
    }
)

admin_list_shift_swagger = swagger_auto_schema(
    operation_summary='List All Operator Shifts (Admin)',
    operation_description=(
        'Allows administrators to retrieve a list of all operator shifts. '
        'Optional search functionality is available using the "search" query parameter to filter by operator username or date. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.operatorprogram.shift'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter shifts by operator username or date.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: OperatorShiftSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# OperatorShiftOperatorAPIView Decorators
operator_retrieve_shift_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Operator Shift',
    operation_description=(
        'Allows operators to retrieve details of their own shift by its ID. '
        'This operation requires JWT authentication and staff role.'
    ),
    tags=['operatorprogram.shift'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the shift to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: OperatorShiftSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only staff members can access their own shifts.',
        404: 'Not Found: Shift with the specified ID does not exist.'
    }
)

operator_list_shift_swagger = swagger_auto_schema(
    operation_summary='List Own Operator Shifts',
    operation_description=(
        'Allows operators to retrieve a list of their own shifts. '
        'This operation requires JWT authentication and staff role.'
    ),
    tags=['operatorprogram.shift'],
    responses={
        200: OperatorShiftSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only staff members can access their own shifts.'
    }
)

operator_active_shifts_swagger = swagger_auto_schema(
    operation_summary='List Active Operator Shifts',
    operation_description=(
        'Allows operators to retrieve a list of their active shifts. '
        'This operation requires JWT authentication and staff role.'
    ),
    tags=['operatorprogram.shift'],
    responses={
        200: OperatorShiftSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only staff members can access their own shifts.'
    }
)

# CancellationPeriodAdminAPIView Decorators
admin_create_cancellation_period_swagger = swagger_auto_schema(
    operation_summary='Create a New Cancellation Period (Admin)',
    operation_description=(
        'Allows administrators to create a new cancellation period. '
        'The request must include laser_area, start_date, and end_date. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.operatorprogram.cancellation_period'],
    request_body=CancellationPeriodSerializer,
    responses={
        201: CancellationPeriodSerializer,
        400: 'Invalid input data (e.g., invalid dates or laser area).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_cancellation_period_swagger = swagger_auto_schema(
    operation_summary='Retrieve Cancellation Period Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a specific cancellation period by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.operatorprogram.cancellation_period'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the cancellation period to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: CancellationPeriodSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Cancellation period with the specified ID does not exist.'
    }
)

admin_update_cancellation_period_swagger = swagger_auto_schema(
    operation_summary='Update Cancellation Period Details (Admin)',
    operation_description=(
        'Allows administrators to fully update a cancellation period identified by its ID. '
        'The request body must include all required fields even if some remain unchanged. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.operatorprogram.cancellation_period'],
    request_body=CancellationPeriodSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the cancellation period to update.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: CancellationPeriodSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Cancellation period with the specified ID does not exist.'
    }
)

admin_list_cancellation_period_swagger = swagger_auto_schema(
    operation_summary='List All Cancellation Periods (Admin)',
    operation_description=(
        'Allows administrators to retrieve a list of all cancellation periods. '
        'Optional search functionality is available using the "search" query parameter to filter by laser area name. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.operatorprogram.cancellation_period'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter cancellation periods by laser area name.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: CancellationPeriodSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# CancellationPeriodUserAPIView Decorators
user_retrieve_cancellation_period_swagger = swagger_auto_schema(
    operation_summary='Retrieve Active Cancellation Period',
    operation_description=(
        'Allows authenticated users to retrieve details of an active cancellation period by its ID. '
        'This operation requires JWT authentication.'
    ),
    tags=['operatorprogram.cancellation_period'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the cancellation period to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: CancellationPeriodSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        404: 'Not Found: Cancellation period with the specified ID does not exist or is not active.'
    }
)

user_list_cancellation_period_swagger = swagger_auto_schema(
    operation_summary='List Active Cancellation Periods',
    operation_description=(
        'Allows authenticated users to retrieve a list of active cancellation periods. '
        'This operation requires JWT authentication.'
    ),
    tags=['operatorprogram.cancellation_period'],
    responses={
        200: CancellationPeriodSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.'
    }
)