from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.reserve.serializers.reserve import ReservationScheduleSerializer, ReservationSerializer, PreReservationSerializer

# ReservationScheduleAdminAPIView Decorators
admin_create_schedule_swagger = swagger_auto_schema(
    operation_summary='Create a New Reservation Schedule (Admin)',
    operation_description=(
        'Allows administrators to create a new reservation schedule. '
        'The request must include operator, date, start_time, and end_time. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.schedule'],
    request_body=ReservationScheduleSerializer,
    responses={
        201: ReservationScheduleSerializer,
        400: 'Invalid input data (e.g., invalid date or time).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_schedule_swagger = swagger_auto_schema(
    operation_summary='Retrieve Reservation Schedule Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a specific reservation schedule by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.schedule'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the schedule to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: ReservationScheduleSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Schedule with the specified ID does not exist.'
    }
)

admin_update_schedule_swagger = swagger_auto_schema(
    operation_summary='Update Reservation Schedule Details (Admin)',
    operation_description=(
        'Allows administrators to fully update a reservation schedule identified by its ID. '
        'The request body must include all required fields even if some remain unchanged. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.schedule'],
    request_body=ReservationScheduleSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the schedule to update.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: ReservationScheduleSerializer,
        400: 'Invalid input data (e.g., invalid date or time).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Schedule with the specified ID does not exist.'
    }
)

admin_list_schedule_swagger = swagger_auto_schema(
    operation_summary='List All Reservation Schedules (Admin)',
    operation_description=(
        'Allows administrators to retrieve a list of all reservation schedules. '
        'Optional search functionality is available using the "search" query parameter to filter by operator username or date. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.schedule'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter schedules by operator username or date.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: ReservationScheduleSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# ReservationScheduleAPIView Decorators
user_list_schedule_swagger = swagger_auto_schema(
    operation_summary='List Available Reservation Schedules',
    operation_description=(
        'Allows authenticated users to retrieve a list of all available reservation schedules. '
        'This operation requires JWT authentication.'
    ),
    tags=['reserve.schedule'],
    responses={
        200: ReservationScheduleSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.'
    }
)

user_retrieve_schedule_swagger = swagger_auto_schema(
    operation_summary='Retrieve Reservation Schedule Details',
    operation_description=(
        'Allows authenticated users to retrieve details of a specific reservation schedule by its ID. '
        'This operation requires JWT authentication.'
    ),
    tags=['reserve.schedule'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the schedule to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: ReservationScheduleSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        404: 'Not Found: Schedule with the specified ID does not exist.'
    }
)

user_available_schedules_swagger = swagger_auto_schema(
    operation_summary='List Available Reservation Schedules for a Date',
    operation_description=(
        'Allows authenticated users to retrieve a list of available reservation schedules for a specific date. '
        'The "date" query parameter is required. '
        'This operation requires JWT authentication.'
    ),
    tags=['reserve.schedule'],
    manual_parameters=[
        openapi.Parameter('date', openapi.IN_QUERY, description="The date to filter available schedules (YYYY-MM-DD).", type=openapi.TYPE_STRING)
    ],
    responses={
        200: ReservationScheduleSerializer(many=True),
        400: 'Bad Request: Date parameter is required.',
        401: 'Unauthorized: Valid JWT token required.'
    }
)

# ReservationAdminAPIView Decorators
admin_create_reservation_swagger = swagger_auto_schema(
    operation_summary='Create a New Reservation (Admin)',
    operation_description=(
        'Allows administrators to create a new reservation. '
        'The request must include user, schedule, and laser_area. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.reservation'],
    request_body=ReservationSerializer,
    responses={
        201: ReservationSerializer,
        400: 'Invalid input data (e.g., invalid schedule or laser area).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_reservation_swagger = swagger_auto_schema(
    operation_summary='Retrieve Reservation Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a specific reservation by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.reservation'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the reservation to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: ReservationSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Reservation with the specified ID does not exist.'
    }
)

admin_update_reservation_swagger = swagger_auto_schema(
    operation_summary='Update Reservation Details (Admin)',
    operation_description=(
        'Allows administrators to fully update a reservation identified by its ID. '
        'The request body must include all required fields even if some remain unchanged. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.reservation'],
    request_body=ReservationSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the reservation to update.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: ReservationSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Reservation with the specified ID does not exist.'
    }
)

admin_list_reservation_swagger = swagger_auto_schema(
    operation_summary='List All Reservations (Admin)',
    operation_description=(
        'Allows administrators to retrieve a list of all reservations. '
        'Optional search functionality is available using the "search" query parameter to filter by user username or schedule date. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.reservation'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter reservations by user username or schedule date.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: ReservationSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_unpaid_reservations_swagger = swagger_auto_schema(
    operation_summary='List Unpaid Reservations (Admin)',
    operation_description=(
        'Allows administrators to retrieve a list of unpaid reservations. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.reservation'],
    responses={
        200: ReservationSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# UserReservationAPIView Decorators
user_create_reservation_swagger = swagger_auto_schema(
    operation_summary='Create a New Reservation',
    operation_description=(
        'Allows customers to create a new reservation. '
        'The request must include schedule and laser_area. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['reserve.customer.reservation'],
    request_body=ReservationSerializer,
    responses={
        201: ReservationSerializer,
        400: 'Invalid input data (e.g., invalid schedule or laser area).',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can create reservations.'
    }
)

user_retrieve_reservation_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Reservation',
    operation_description=(
        'Allows customers to retrieve details of their own reservation by its ID. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['reserve.customer.reservation'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the reservation to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: ReservationSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can access their own reservations.',
        404: 'Not Found: Reservation with the specified ID does not exist.'
    }
)

user_list_reservation_swagger = swagger_auto_schema(
    operation_summary='List Own Reservations',
    operation_description=(
        'Allows customers to retrieve a list of their own reservations. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['reserve.customer.reservation'],
    responses={
        200: ReservationSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can access their own reservations.'
    }
)

# OperatorReservationAPIView Decorators
operator_retrieve_reservation_swagger = swagger_auto_schema(
    operation_summary='Retrieve Assigned Reservation',
    operation_description=(
        'Allows operators to retrieve details of a reservation assigned to their schedule by its ID. '
        'This operation requires JWT authentication and staff role.'
    ),
    tags=['reserve.operator.reservation'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the reservation to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: ReservationSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only staff members can access their assigned reservations.',
        404: 'Not Found: Reservation with the specified ID does not exist.'
    }
)

operator_list_reservation_swagger = swagger_auto_schema(
    operation_summary='List Assigned Reservations',
    operation_description=(
        'Allows operators to retrieve a list of reservations assigned to their schedule. '
        'This operation requires JWT authentication and staff role.'
    ),
    tags=['reserve.operator.reservation'],
    responses={
        200: ReservationSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only staff members can access their assigned reservations.'
    }
)

operator_mark_complete_swagger = swagger_auto_schema(
    operation_summary='Mark Reservation as Completed',
    operation_description=(
        'Allows operators to mark a reservation assigned to their schedule as completed. '
        'This operation requires JWT authentication and staff role.'
    ),
    tags=['reserve.operator.reservation'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the reservation to mark as completed.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: ReservationSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only staff members can mark their assigned reservations as completed.',
        404: 'Not Found: Reservation with the specified ID does not exist.'
    }
)

# PreReservationAdminAPIView Decorators
admin_create_pre_reservation_swagger = swagger_auto_schema(
    operation_summary='Create a New Pre-Reservation (Admin)',
    operation_description=(
        'Allows administrators to create a new pre-reservation. '
        'The request must include user, laser_area, and date. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.pre_reservation'],
    request_body=PreReservationSerializer,
    responses={
        201: PreReservationSerializer,
        400: 'Invalid input data (e.g., invalid date or laser area).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_pre_reservation_swagger = swagger_auto_schema(
    operation_summary='Retrieve Pre-Reservation Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a specific pre-reservation by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.pre_reservation'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the pre-reservation to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: PreReservationSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Pre-reservation with the specified ID does not exist.'
    }
)

admin_update_pre_reservation_swagger = swagger_auto_schema(
    operation_summary='Update Pre-Reservation Details (Admin)',
    operation_description=(
        'Allows administrators to fully update a pre-reservation identified by its ID. '
        'The request body must include all required fields even if some remain unchanged. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.pre_reservation'],
    request_body=PreReservationSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the pre-reservation to update.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: PreReservationSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Pre-reservation with the specified ID does not exist.'
    }
)

admin_list_pre_reservation_swagger = swagger_auto_schema(
    operation_summary='List All Pre-Reservations (Admin)',
    operation_description=(
        'Allows administrators to retrieve a list of all pre-reservations. '
        'Optional search functionality is available using the "search" query parameter to filter by user username. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.reserve.pre_reservation'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter pre-reservations by user username.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: PreReservationSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# PreReservationUserAPIView Decorators
user_retrieve_pre_reservation_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Pre-Reservation',
    operation_description=(
        'Allows customers to retrieve details of their own pre-reservation by its ID. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['reserve.customer.pre_reservation'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the pre-reservation to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: PreReservationSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can access their own pre-reservations.',
        404: 'Not Found: Pre-reservation with the specified ID does not exist.'
    }
)

user_list_pre_reservation_swagger = swagger_auto_schema(
    operation_summary='List Own Pre-Reservations',
    operation_description=(
        'Allows customers to retrieve a list of their own pre-reservations. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['reserve.customer.pre_reservation'],
    responses={
        200: PreReservationSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can access their own pre-reservations.'
    }
)