from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
from .models import CustomUser, StaffAttendance, CustomerProfile, Comments, UserRole
from apps.lazer_area.models import LaserArea
from .serializers import CustomUserSerializer


class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create users
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass123', role=UserRole.ADMIN
        )
        self.customer_user = CustomUser.objects.create_user(
            username='customer', email='customer@example.com', password='customerpass123', role=UserRole.CUSTOMER
        )
        self.operator_user = CustomUser.objects.create_user(
            username='operator', email='operator@example.com', password='operatorpass123', role=UserRole.STAFF
        )
        # Create related data
        self.laser_area = LaserArea.objects.create(name='TestArea', current_price=100.00, is_active=True)
        self.customer_profile = CustomerProfile.objects.create(user=self.customer_user, national_id='1234567890', address='test adderess ', house_number='215555555')
        self.staff_attendance = StaffAttendance.objects.create(user=self.operator_user, entry_timestamp=timezone.now())
        self.comment = Comments.objects.create(user=self.customer_user, message='Test comment', is_reviewed=False)

        # Create API clients
        self.admin_client = APIClient()
        self.customer_client = APIClient()
        self.operator_client = APIClient()
        self.unauthenticated_client = APIClient()
        # Generate JWT tokens
        admin_refresh = RefreshToken.for_user(self.admin_user)
        customer_refresh = RefreshToken.for_user(self.customer_user)
        operator_refresh = RefreshToken.for_user(self.operator_user)
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_refresh.access_token}')
        self.customer_client.credentials(HTTP_AUTHORIZATION=f'Bearer {customer_refresh.access_token}')
        self.operator_client.credentials(HTTP_AUTHORIZATION=f'Bearer {operator_refresh.access_token}')

    # CustomUser Admin Tests
    def test_admin_create_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'role': UserRole.CUSTOMER
        }
        response = self.admin_client.post(reverse('core:admin-user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 4)
        self.assertEqual(response.data['username'], 'newuser')

    def test_admin_create_user_invalid(self):
        data = {'username': '', 'email': 'invalid', 'role': 'INVALID_ROLE'}
        response = self.admin_client.post(reverse('core:admin-user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_user(self):
        response = self.admin_client.get(reverse('core:admin-user-detail', kwargs={'id': self.customer_user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.customer_user.id)

    def test_admin_update_user(self):
        data = {
            'username': 'updatedcustomer',
            'email': 'updatedcustomer@example.com',
            'role': UserRole.CUSTOMER
        }
        response = self.admin_client.put(
            reverse('core:admin-user-detail', kwargs={'id': self.customer_user.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer_user.refresh_from_db()
        self.assertEqual(self.customer_user.username, 'updatedcustomer')

    def test_admin_partial_update_user(self):
        data = {'email': 'partialupdate@example.com'}
        response = self.admin_client.patch(
            reverse('core:admin-user-detail', kwargs={'id': self.customer_user.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer_user.refresh_from_db()
        self.assertEqual(self.customer_user.email, 'partialupdate@example.com')

    def test_admin_delete_user(self):
        response = self.admin_client.delete(reverse('core:admin-user-detail', kwargs={'id': self.customer_user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_admin_list_users(self):
        response = self.admin_client.get(reverse('core:admin-user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_customer_access_admin_user_view(self):
        response = self.customer_client.get(reverse('core:admin-user-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # User Profile Tests
    def test_customer_retrieve_own_profile(self):
        response = self.customer_client.get(reverse('core:user-profile-detail', kwargs={'id': self.customer_user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.customer_user.id)

    def test_customer_retrieve_other_profile(self):
        response = self.customer_client.get(reverse('core:user-profile-detail', kwargs={'id': self.admin_user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_partial_update_own_profile(self):
        data = {'email': 'newcustomer@example.com'}
        response = self.customer_client.patch(
            reverse('core:user-profile-detail', kwargs={'id': self.customer_user.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer_user.refresh_from_db()
        self.assertEqual(self.customer_user.email, 'newcustomer@example.com')

    def test_customer_partial_update_other_profile(self):
        data = {'email': 'hacked@example.com'}
        response = self.customer_client.patch(
            reverse('core:user-profile-detail', kwargs={'id': self.admin_user.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Staff Attendance Admin Tests
    def test_admin_create_attendance(self):
        data = {'user_id': self.operator_user.id, 'check_in': timezone.now().isoformat()}
        response = self.admin_client.post(reverse('core:admin-staff-attendance-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StaffAttendance.objects.count(), 2)

    def test_admin_retrieve_attendance(self):
        response = self.admin_client.get(
            reverse('core:admin-staff-attendance-detail', kwargs={'id': self.staff_attendance.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.staff_attendance.id))

    def test_admin_update_attendance(self):
        data = {'user_id': self.operator_user.id, 'check_in': (timezone.now() - timedelta(hours=1)).isoformat()}
        response = self.admin_client.put(
            reverse('core:admin-staff-attendance-detail', kwargs={'id': self.staff_attendance.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_list_attendance(self):
        response = self.admin_client.get(reverse('core:admin-staff-attendance-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Staff Attendance Operator Tests
    def test_operator_retrieve_own_attendance(self):
        response = self.operator_client.get(
            reverse('core:operator-staff-attendance-detail', kwargs={'id': self.staff_attendance.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.staff_attendance.id))

    def test_operator_retrieve_other_attendance(self):
        other_attendance = StaffAttendance.objects.create(user=self.admin_user, entry_timestamp=timezone.now())
        response = self.operator_client.get(
            reverse('core:operator-staff-attendance-detail', kwargs={'id': other_attendance.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_operator_list_own_attendance(self):
        response = self.operator_client.get(reverse('core:operator-staff-attendance-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Customer Profile Admin Tests
    def test_admin_create_customer_profile(self):
        new_user = CustomUser.objects.create_user(
            username='newcustomer', email='newcustomer@example.com', password='pass123', role=UserRole.CUSTOMER
        )
        data = {'user_id': new_user.id, 'national_id': '0987654321', 'address': 'test adderess ', 'house_number': '555128155'}
        response = self.admin_client.post(reverse('core:admin-customer-profile-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomerProfile.objects.count(), 2)

    def test_admin_retrieve_customer_profile(self):
        response = self.admin_client.get(
            reverse('core:admin-customer-profile-detail', kwargs={'id': self.customer_profile.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.customer_profile.id)

    def test_admin_update_customer_profile(self):
        data = {'user_id': self.customer_user.id, 'national_id': '1111111111', 'address': 'test adderess ', 'house_number': '555128155'}

        response = self.admin_client.put(
            reverse('core:admin-customer-profile-detail', kwargs={'id': self.customer_profile.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer_profile.refresh_from_db()
        self.assertEqual(self.customer_profile.national_id, '1111111111')

    def test_admin_list_customer_profiles(self):
        response = self.admin_client.get(reverse('core:admin-customer-profile-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Customer Profile Customer Tests
    def test_customer_retrieve_own_customer_profile(self):
        response = self.customer_client.get(
            reverse('core:customer-profile-detail', kwargs={'id': self.customer_profile.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.customer_profile.id)

    def test_customer_retrieve_other_customer_profile(self):
        other_profile = CustomerProfile.objects.create(
            user=self.operator_user, national_id='2222222222', address='test adderess ', house_number='215555555'
        )
        response = self.customer_client.get(
            reverse('core:customer-profile-detail', kwargs={'id': other_profile.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_partial_update_own_customer_profile(self):
        data = {'national_id': '3333333333'}
        response = self.customer_client.patch(
            reverse('core:customer-profile-detail', kwargs={'id': self.customer_profile.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer_profile.refresh_from_db()
        self.assertEqual(self.customer_profile.national_id, '3333333333')

    # Comments Admin Tests
    def test_admin_create_comment(self):
        data = {
            'user_id': self.customer_user.id,
            'laser_area_id': self.laser_area.id,
            'message': 'New admin comment',
            'is_reviewed': False
        }
        response = self.admin_client.post(reverse('core:admin-comment-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comments.objects.count(), 2)

    def test_admin_retrieve_comment(self):
        response = self.admin_client.get(
            reverse('core:admin-comment-detail', kwargs={'id': self.comment.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.comment.id))

    def test_admin_update_comment(self):
        data = {
            'user_id': self.customer_user.id,
            'laser_area_id': self.laser_area.id,
            'message': 'Updated comment',
            'is_reviewed': True
        }
        response = self.admin_client.put(
            reverse('core:admin-comment-detail', kwargs={'id': self.comment.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.message, 'Updated comment')

    def test_admin_list_comments(self):
        response = self.admin_client.get(reverse('core:admin-comment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_unreviewed_comments(self):
        response = self.admin_client.get(reverse('core:admin-comment-unreviewed'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Comments Customer Tests
    def test_customer_create_comment(self):
        custom_user_serializer = CustomUserSerializer(self.customer_user, many=False)
        data = {'laser_area_id': self.laser_area.id, 'message': 'Customer comment', 'user': custom_user_serializer.data, 'user_id': custom_user_serializer.data['id']}
        response = self.customer_client.post(reverse('core:comment-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comments.objects.count(), 2)

    def test_customer_retrieve_own_comment(self):
        response = self.customer_client.get(
            reverse('core:comment-detail', kwargs={'id': self.comment.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.comment.id))

    def test_customer_retrieve_other_comment(self):
        other_comment = Comments.objects.create(
            user=self.operator_user, message='Other comment'
        )
        response = self.customer_client.get(
            reverse('core:comment-detail', kwargs={'id': other_comment.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_list_own_comments(self):
        response = self.customer_client.get(reverse('core:comment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_operator_create_comment(self):
        data = {'laser_area_id': self.laser_area.id, 'message': 'Operator comment'}
        response = self.operator_client.post(reverse('core:comment-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Unauthenticated Access Tests
    def test_unauthenticated_access(self):
        response = self.unauthenticated_client.get(reverse('core:admin-user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)