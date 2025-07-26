from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.core.serializers import CustomUserSerializer, StaffAttendanceSerializer, CustomerProfileSerializer, CommentsSerializer

# UserAdminAPIView Decorators
admin_create_user_swagger = swagger_auto_schema(
    operation_summary='Create a New User (Admin)',
    operation_description=(
        'Allows administrators to create a new user. '
        'The request must include username, email, role, and optional password. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.user'],
    request_body=CustomUserSerializer,
    responses={
        201: CustomUserSerializer,
        400: 'Invalid input data (e.g., invalid role, missing username).',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_user_swagger = swagger_auto_schema(
    operation_summary='Retrieve User Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a specific user by their ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.user'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the user to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomUserSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: User with the specified ID does not exist.'
    }
)

admin_update_user_swagger = swagger_auto_schema(
    operation_summary='Fully Update a User (Admin)',
    operation_description=(
        'Allows administrators to fully update a user’s details by their ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.user'],
    request_body=CustomUserSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the user to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomUserSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: User with the specified ID does not exist.'
    }
)

admin_partial_update_user_swagger = swagger_auto_schema(
    operation_summary='Partially Update a User (Admin)',
    operation_description=(
        'Allows administrators to partially update a user’s details by their ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.user'],
    request_body=CustomUserSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the user to partially update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomUserSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: User with the specified ID does not exist.'
    }
)

admin_destroy_user_swagger = swagger_auto_schema(
    operation_summary='Delete a User (Admin)',
    operation_description=(
        'Allows administrators to delete a user by their ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.user'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the user to delete.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: 'User successfully deleted.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: User with the specified ID does not exist.'
    }
)

admin_list_user_swagger = swagger_auto_schema(
    operation_summary='List All Users (Admin)',
    operation_description=(
        'Allows administrators to retrieve a list of all users. '
        'Optional search functionality is available using the "search" query parameter to filter by username, email, or role. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.user'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter users by username, email, or role.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: CustomUserSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# UserProfileAPIView Decorators
user_retrieve_profile_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Profile',
    operation_description=(
        'Allows authenticated users to retrieve their own profile details. '
        'This operation requires JWT authentication.'
    ),
    tags=['core.user'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the user’s profile to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomUserSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only access their own profile.',
        404: 'Not Found: Profile does not exist.'
    }
)

user_update_profile_swagger = swagger_auto_schema(
    operation_summary='Partially Update Own Profile',
    operation_description=(
        'Allows authenticated users to partially update their own profile details. '
        'This operation requires JWT authentication.'
    ),
    tags=['core.user'],
    request_body=CustomUserSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the user’s profile to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomUserSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: User can only update their own profile.',
        404: 'Not Found: Profile does not exist.'
    }
)

# StaffAttendanceAdminAPIView Decorators
admin_create_attendance_swagger = swagger_auto_schema(
    operation_summary='Create a New Attendance Record (Admin)',
    operation_description=(
        'Allows administrators to create a new staff attendance record. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.attendance'],
    request_body=StaffAttendanceSerializer,
    responses={
        201: StaffAttendanceSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_attendance_swagger = swagger_auto_schema(
    operation_summary='Retrieve Attendance Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a specific attendance record by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.attendance'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the attendance record to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: StaffAttendanceSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Attendance record does not exist.'
    }
)

admin_update_attendance_swagger = swagger_auto_schema(
    operation_summary='Update Attendance Details (Admin)',
    operation_description=(
        'Allows administrators to update an attendance record by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.attendance'],
    request_body=StaffAttendanceSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the attendance record to update.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: StaffAttendanceSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Attendance record does not exist.'
    }
)

admin_list_attendance_swagger = swagger_auto_schema(
    operation_summary='List All Attendance Records (Admin)',
    operation_description=(
        'Lists all staff attendance records. '
        'Optional search functionality is available using the "search" query parameter to filter by username. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.attendance'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter attendance by username.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: StaffAttendanceSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# StaffAttendanceOperatorAPIView Decorators
operator_retrieve_attendance_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Attendance Record',
    operation_description=(
        'Allows operators to retrieve their own attendance record by its ID. '
        'This operation requires JWT authentication and staff role.'
    ),
    tags=['core.operator.attendance'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the attendance record to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: StaffAttendanceSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only staff members can access their own attendance records.',
        404: 'Not Found: Attendance record does not exist.'
    }
)

operator_list_attendance_swagger = swagger_auto_schema(
    operation_summary='List Own Attendance Records',
    operation_description=(
        'Lists all attendance records for the authenticated operator. '
        'This operation requires JWT authentication and staff role.'
    ),
    tags=['core.operator.attendance'],
    responses={
        200: StaffAttendanceSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only staff members can access their own attendance records.'
    }
)

# CustomerProfileAdminAPIView Decorators
admin_create_customer_profile_swagger = swagger_auto_schema(
    operation_summary='Create a New Customer Profile (Admin)',
    operation_description=(
        'Allows administrators to create a new customer profile. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.customer_profile'],
    request_body=CustomerProfileSerializer,
    responses={
        201: CustomerProfileSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_customer_profile_swagger = swagger_auto_schema(
    operation_summary='Retrieve Customer Profile Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a specific customer profile by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.customer_profile'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the customer profile to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomerProfileSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Customer profile does not exist.'
    }
)

admin_update_customer_profile_swagger = swagger_auto_schema(
    operation_summary='Update Customer Profile Details (Admin)',
    operation_description=(
        'Allows administrators to update a customer profile by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.customer_profile'],
    request_body=CustomerProfileSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the customer profile to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomerProfileSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Customer profile does not exist.'
    }
)

admin_list_customer_profile_swagger = swagger_auto_schema(
    operation_summary='List All Customer Profiles (Admin)',
    operation_description=(
        'Lists all customer profiles. '
        'Optional search functionality is available using the "search" query parameter to filter by national_id or username. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.customer_profile'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter customer profiles by national_id or username.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: CustomerProfileSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# CustomerProfileUserAPIView Decorators
user_retrieve_customer_profile_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Customer Profile',
    operation_description=(
        'Allows customers to view their own profile details. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['core.customer_profile'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the customer profile to retrieve.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomerProfileSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can access their own profile.',
        404: 'Not Found: Customer profile does not exist.'
    }
)

user_update_customer_profile_swagger = swagger_auto_schema(
    operation_summary='Partially Update Own Customer Profile',
    operation_description=(
        'Allows customers to partially update their own profile details. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['core.customer_profile'],
    request_body=CustomerProfileSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the customer profile to update.", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: CustomerProfileSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can update their own profile.',
        404: 'Not Found: Customer profile does not exist.'
    }
)

# CommentsAdminAPIView Decorators
admin_create_comment_swagger = swagger_auto_schema(
    operation_summary='Create a New Comment (Admin)',
    operation_description=(
        'Allows administrators to create a new comment. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.comment'],
    request_body=CommentsSerializer,
    responses={
        201: CommentsSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_retrieve_comment_swagger = swagger_auto_schema(
    operation_summary='Retrieve Comment Details (Admin)',
    operation_description=(
        'Allows administrators to retrieve detailed information about a specific comment by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.comment'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The unique ID of the comment to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: CommentsSerializer,
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Comment does not exist.'
    }
)

admin_update_comment_swagger = swagger_auto_schema(
    operation_summary='Update Comment Details (Admin)',
    operation_description=(
        'Allows administrators to update a comment by its ID. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.comment'],
    request_body=CommentsSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the comment to update.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: CommentsSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.',
        404: 'Not Found: Comment does not exist.'
    }
)

admin_list_comment_swagger = swagger_auto_schema(
    operation_summary='List All Comments (Admin)',
    operation_description=(
        'Lists all comments. '
        'Optional search functionality is available using the "search" query parameter to filter by message or username. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.comment'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Filter comments by message or username.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: CommentsSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

admin_unreviewed_comments_swagger = swagger_auto_schema(
    operation_summary='List Unreviewed Comments (Admin)',
    operation_description=(
        'Allows administrators to retrieve a list of unreviewed comments. '
        'This operation is restricted to admin users only and requires JWT authentication.'
    ),
    tags=['admin.core.comment'],
    responses={
        200: CommentsSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required for admin users.',
        403: 'Forbidden: User is not an admin.'
    }
)

# CommentsUserAPIView Decorators
user_create_comment_swagger = swagger_auto_schema(
    operation_summary='Create a New Comment',
    operation_description=(
        'Allows customers to submit a new comment. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['core.customer.comment'],
    request_body=CommentsSerializer,
    responses={
        201: CommentsSerializer,
        400: 'Invalid input data.',
        401: 'Unauthorized: Valid user JWT authentication required.',
403: 'Forbidden: Only customers can perform this action.',
    }
)

user_retrieve_comment_swagger = swagger_auto_schema(
    operation_summary='Retrieve Own Comment',
    operation_description=(
        'Allows customers to retrieve their own comment by its ID. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['core.customer.comment'],
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the comment to retrieve.", type=openapi.TYPE_STRING)
    ],
    responses={
        200: CommentsSerializer,
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can access their own comments.',
        404: 'Not Found: Comment does not exist.'
    }
)

user_list_comment_swagger = swagger_auto_schema(
    operation_summary='List Own Comments',
    operation_description=(
        'Allows customers to list their own comments. '
        'This operation requires JWT authentication and customer role.'
    ),
    tags=['core.customer.comment'],
    responses={
        200: CommentsSerializer(many=True),
        401: 'Unauthorized: Valid JWT token required.',
        403: 'Forbidden: Only customers can access their own comments.'
    }
)