from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.lazer_area.serializers import LaserAreaSerializer, LaserAreaScheduleSerializer

# LaserAreaAdminAPIView Decorators
admin_create_laser_area_swagger = swagger_auto_schema(
    operation_summary='Create a New Laser Area (Admin)',
    operation_description=(
        'Allows administrators to create a new laser treatment area. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.lazerapp.laser_area'],
    request_body=LaserAreaSerializer,
    responses={
        201: LaserAreaSerializer,
        400: 'Invalid input data (e.g., negative price).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_laser_area_swagger = swagger_auto_schema(
    operation_summary='Retrieve Laser Area Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a laser area by its name. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.lazerapp.laser_area'],
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_PATH, description="The name of the laser area to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: LaserAreaSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Laser area does not exist.'
    }
)

admin_update_laser_area_swagger = swagger_auto_schema(
    operation_summary='Update Laser Area Details (Admin)',
    operation_description=(
        'Allows administrators to update a laser area by its name. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.lazerapp.laser_area'],
    request_body=LaserAreaSerializer,
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_PATH, description="The name of the laser area to update.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: LaserAreaSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Laser area does not exist.'
    }
)

admin_destroy_laser_area_swagger = swagger_auto_schema(
    operation_summary='Delete a Laser Area (Admin)',
    operation_description=(
        'Allows administrators to delete a laser area by its name. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.lazerapp.laser_area'],
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_PATH, description="The name of the laser area to delete.", type=openapi.TYPE_STRING)
    ],
    responses={
        204: 'Laser area deleted successfully.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Laser area does not exist.'
    }
)

admin_list_laser_area_swagger = swagger_auto_schema(
    operation_summary='List All Laser Areas (Admin)',
    operation_description=(
        'Lists all laser areas. '
        'Optional search functionality is available using the "search" query parameter to filter by name. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.lazerapp.laser_area'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter laser areas by name.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: LaserAreaSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# LaserAreaUserAPIView Decorators
user_list_laser_area_swagger = swagger_auto_schema(
    operation_summary='List Active Laser Areas',
    operation_description=(
        'Allows authenticated users to list all active laser areas. '
        'This operation requires JWT authentication.'
    ),
    tags=['lazerapp.laser_area'],
    responses={
        200: LaserAreaSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.'
    }
)

user_retrieve_laser_area_swagger = swagger_auto_schema(
    operation_summary='Retrieve Active Laser Area',
    operation_description=(
        'Allows authenticated users to retrieve details of an active laser area by its name. '
        'This operation requires JWT authentication.'
    ),
    tags=['lazerapp.laser_area'],
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_PATH, description="The name of the laser area to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: LaserAreaSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        404: 'Not Found: Laser area not found or not active.'
    }
)

# LaserAreaScheduleAdminAPIView Decorators
admin_create_laser_schedule_swagger = swagger_auto_schema(
    operation_summary='Create a New Laser Schedule (Admin)',
    operation_description=(
        'Allows administrators to create a new laser area schedule. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.lazerapp.laser_schedule'],
    request_body=LaserAreaScheduleSerializer,
    responses={
        201: LaserAreaScheduleSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_laser_schedule_swagger = swagger_auto_schema(
    operation_summary='Retrieve Laser Schedule Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a laser schedule by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.lazerapp.laser_schedule'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the laser schedule to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: LaserAreaScheduleSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Laser schedule does not exist.'
    }
)

admin_update_laser_schedule_swagger = swagger_auto_schema(
    operation_summary='Update Laser Schedule Details (Admin)',
    operation_description=(
        'Allows administrators to update a laser schedule by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.lazerapp.laser_schedule'],
    request_body=LaserAreaScheduleSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the laser schedule to update.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: LaserAreaScheduleSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Laser schedule does not exist.'
    }
)

admin_list_laser_schedule_swagger = swagger_auto_schema(
    operation_summary='List All Laser Schedules (Admin)',
    operation_description=(
        'Lists all laser schedules. '
        'Optional search functionality is available using the "search" query parameter to filter by laser area name. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.lazerapp.laser_schedule'],
    responses={
        200: LaserAreaScheduleSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# LaserAreaScheduleUserAPIView Decorators
user_list_laser_schedule_swagger = swagger_auto_schema(
    operation_summary='List Available Laser Schedules',
    operation_description=(
        'Allows authenticated users to list available laser schedules. '
        'This operation requires JWT authentication.'
    ),
    tags=['lazerapp.laser_schedule'],
    responses={
        200: LaserAreaScheduleSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.'
    }
)

user_retrieve_laser_schedule_swagger = swagger_auto_schema(
    operation_summary='Retrieve Laser Schedule',
    operation_description=(
        'Allows authenticated users to retrieve details of a laser schedule by its ID. '
        'This operation requires JWT authentication.'
    ),
    tags=['lazerapp.laser_schedule'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the laser schedule to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: LaserAreaScheduleSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        404: 'Not Found: Laser schedule does not exist or not available.'
    }
)

user_active_schedules_swagger = swagger_auto_schema(
    operation_summary='List Active Laser Schedules',
    operation_description=(
        'Allows authenticated users to retrieve a list of active laser schedules. '
        'This operation requires authentication.'
    ),
    tags=['lazerapp.laser_schedule'],
    responses={
        200: LaserAreaScheduleSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.'
    }
)