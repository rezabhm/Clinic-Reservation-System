from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
from .models import LaserArea, LaserAreaSchedule
from apps.core.models import CustomUser, UserRole
from .serializers import LaserAreaSerializer


class LazerAppViewsTestCase(TestCase):
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
        self.laser_schedule = LaserAreaSchedule.objects.create(
            laser_area=self.laser_area, start_time=timezone.now() + timedelta(hours=1),
            price=100000.00
        )
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

    # LaserArea Admin Tests
    def test_admin_create_laser_area(self):
        data = {'name': 'NewArea', 'price': 150.00, 'is_active': True}
        response = self.admin_client.post(reverse('lazerapp:admin-laser-area-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LaserArea.objects.count(), 2)
        self.assertEqual(response.data['name'], 'NewArea')

    def test_admin_create_laser_area_invalid(self):
        data = {'name': '', 'price': -10.00}
        response = self.admin_client.post(reverse('lazerapp:admin-laser-area-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_laser_area(self):
        response = self.admin_client.get(
            reverse('lazerapp:admin-laser-area-detail', kwargs={'name': self.laser_area.name})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.laser_area.name)

    def test_admin_update_laser_area(self):
        data = {'name': 'UpdatedArea', 'price': 200.00, 'is_active': False}
        response = self.admin_client.put(
            reverse('lazerapp:admin-laser-area-detail', kwargs={'name': self.laser_area.name}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.laser_area.refresh_from_db()
        self.assertEqual(self.laser_area.name, 'UpdatedArea')

    def test_admin_delete_laser_area(self):
        response = self.admin_client.delete(
            reverse('lazerapp:admin-laser-area-detail', kwargs={'name': self.laser_area.name})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(LaserArea.objects.count(), 0)

    def test_admin_list_laser_areas(self):
        response = self.admin_client.get(reverse('lazerapp:admin-laser-area-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # LaserArea User Tests
    def test_customer_list_laser_areas(self):
        response = self.customer_client.get(reverse('lazerapp:laser-area-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_customer_retrieve_laser_area(self):
        response = self.customer_client.get(
            reverse('lazerapp:laser-area-detail', kwargs={'name': self.laser_area.name})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.laser_area.name)

    def test_customer_retrieve_inactive_laser_area(self):
        inactive_area = LaserArea.objects.create(name='InactiveArea', current_price=50.00, is_active=False)
        response = self.customer_client.get(
            reverse('lazerapp:laser-area-detail', kwargs={'name': inactive_area.name})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # LaserAreaSchedule Admin Tests
    def test_admin_create_laser_schedule(self):
        laser_area_serializer = LaserAreaSerializer(self.laser_area, many=False)

        data = {
            'laser_area_name': self.laser_area.id,
            'laser_area': laser_area_serializer.data,
            'start_time': (timezone.now() + timedelta(hours=2)).isoformat()
        }
        response = self.admin_client.post(reverse('lazerapp:admin-laser-schedule-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LaserAreaSchedule.objects.count(), 2)

    def test_admin_retrieve_laser_schedule(self):
        response = self.admin_client.get(
            reverse('lazerapp:admin-laser-schedule-detail', kwargs={'id': self.laser_schedule.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.laser_schedule.id))

    def test_admin_update_laser_schedule(self):
        data = {
            'laser_area_name': self.laser_area.id,
            'start_time': (timezone.now() + timedelta(hours=3)).isoformat()
        }
        response = self.admin_client.put(
            reverse('lazerapp:admin-laser-schedule-detail', kwargs={'id': self.laser_schedule.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_list_laser_schedules(self):
        response = self.admin_client.get(reverse('lazerapp:admin-laser-schedule-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # LaserAreaSchedule User Tests
    def test_customer_list_laser_schedules(self):
        response = self.customer_client.get(reverse('lazerapp:laser-schedule-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_customer_retrieve_laser_schedule(self):
        response = self.customer_client.get(
            reverse('lazerapp:laser-schedule-detail', kwargs={'id': self.laser_schedule.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.laser_schedule.id))

    def test_customer_active_schedules(self):
        response = self.customer_client.get(reverse('lazerapp:laser-schedule-active'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_access(self):
        response = self.unauthenticated_client.get(reverse('lazerapp:laser-area-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)