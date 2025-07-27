from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
from apps.core.models import CustomUser, UserRole
from apps.reserve.models.program import OperatorShift, CancellationPeriod

class OperatorShiftCancellationViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass123', role=UserRole.ADMIN
        )
        self.operator_user = CustomUser.objects.create_user(
            username='operator', email='operator@example.com', password='operatorpass123', role=UserRole.STAFF
        )
        self.customer_user = CustomUser.objects.create_user(
            username='customer', email='customer@example.com', password='customerpass123', role=UserRole.CUSTOMER
        )

        # Create API clients with JWT tokens
        self.admin_client = APIClient()
        self.operator_client = APIClient()
        self.customer_client = APIClient()

        admin_token = RefreshToken.for_user(self.admin_user)
        operator_token = RefreshToken.for_user(self.operator_user)
        customer_token = RefreshToken.for_user(self.customer_user)

        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token.access_token}')
        self.operator_client.credentials(HTTP_AUTHORIZATION=f'Bearer {operator_token.access_token}')
        self.customer_client.credentials(HTTP_AUTHORIZATION=f'Bearer {customer_token.access_token}')

        # Create an operator shift
        self.shift = OperatorShift.objects.create(
            operator=self.operator_user,
            operator_name=self.operator_user.username,
            shift_date=timezone.now().date() + timedelta(days=1),
            period='MORNING'
        )

        # Create a cancellation period
        self.cancellation = CancellationPeriod.objects.create(
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=2)
        )

    # ------------------- OperatorShift Admin -------------------
    def test_admin_create_shift(self):
        data = {
            'operator_id': self.operator_user.id,
            'shift_date': (timezone.now().date() + timedelta(days=2)).isoformat(),
            'period': 'AFTERNOON',
        }
        response = self.admin_client.post(reverse('reserve:admin-operator-shift-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_retrieve_shift(self):
        response = self.admin_client.get(
            reverse('reserve:admin-operator-shift-detail', kwargs={'id': self.shift.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_update_shift(self):
        data = {
            'operator_id': self.operator_user.id,
            'shift_date': (timezone.now().date() + timedelta(days=3)).isoformat(),
            'period': 'MORNING',
        }
        response = self.admin_client.put(
            reverse('reserve:admin-operator-shift-detail', kwargs={'id': self.shift.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_list_shifts(self):
        response = self.admin_client.get(reverse('reserve:admin-operator-shift-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # ------------------- OperatorShift Operator -------------------
    def test_operator_list_own_shifts(self):
        response = self.operator_client.get(reverse('reserve:operator-shift-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_operator_retrieve_own_shift(self):
        response = self.operator_client.get(
            reverse('reserve:operator-shift-detail', kwargs={'id': self.shift.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_operator_cannot_retrieve_others_shift(self):
        shift = OperatorShift.objects.create(
            operator=self.admin_user,
            operator_name='admin',
            shift_date=timezone.now().date() + timedelta(days=1),
            period='MORNING'
        )
        response = self.operator_client.get(
            reverse('reserve:operator-shift-detail', kwargs={'id': shift.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_operator_active_shifts(self):
        response = self.operator_client.get(reverse('reserve:operator-shift-active'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    # ------------------- CancellationPeriod Admin -------------------
    def test_admin_create_cancellation_period(self):
        data = {
            'start_time': (timezone.now() + timedelta(hours=3)).isoformat(),
            'end_time': (timezone.now() + timedelta(hours=4)).isoformat()
        }
        response = self.admin_client.post(reverse('reserve:admin-cancellation-period-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_retrieve_cancellation_period(self):
        response = self.admin_client.get(
            reverse('reserve:admin-cancellation-period-detail', kwargs={'id': self.cancellation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_update_cancellation_period(self):
        data = {
            'start_time': (timezone.now() + timedelta(hours=5)).isoformat(),
            'end_time': (timezone.now() + timedelta(hours=6)).isoformat()
        }
        response = self.admin_client.put(
            reverse('reserve:admin-cancellation-period-detail', kwargs={'id': self.cancellation.id}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_list_cancellation_periods(self):
        response = self.admin_client.get(reverse('reserve:admin-cancellation-period-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # ------------------- CancellationPeriod User -------------------
    def test_user_list_active_cancellation_periods(self):
        response = self.customer_client.get(reverse('reserve:cancellation-period-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_user_retrieve_active_cancellation_period(self):
        response = self.customer_client.get(
            reverse('reserve:cancellation-period-detail', kwargs={'id': self.cancellation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access_denied(self):
        unauthenticated = APIClient()
        response = unauthenticated.get(reverse('reserve:operator-shift-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)