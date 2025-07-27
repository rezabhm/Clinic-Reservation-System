from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
from apps.reserve.models.reserve import ReservationSchedule, Reservation, PreReservation
from apps.core.models import CustomUser, UserRole
from apps.lazer_area.models import LaserArea, LaserAreaSchedule


class ReserveViewsTestCase(TestCase):
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
        self.schedule = ReservationSchedule.objects.create(
            operator=self.operator_user, date=timezone.now().date(),
            period='MORNING', time_slot='8-10', duration=30
        )
        self.reservation = Reservation.objects.create(
            user=self.customer_user, schedule=self.schedule, laser_area=self.laser_area,
            session_number=1, total_price=1000.00, final_amount=1000.00, is_paid=False
        )
        self.reservation.laser_area_schedules.add(self.laser_schedule)
        self.pre_reservation = PreReservation.objects.create(
            user=self.customer_user, laser_area_schedule=self.laser_schedule,
            session_count=10, last_session_date=timezone.now().date() + timedelta(days=1)
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

    # ReservationSchedule Admin Tests
    def test_admin_create_schedule(self):
        data = {
            'operator_id': self.operator_user.id,
            'date': (timezone.now().date() + timedelta(days=1)).isoformat(),
            'period': 'MORNING',
            'time_slot': '10-12',
            'duration': 30
        }
        response = self.admin_client.post(reverse('reserve:admin-reservation-schedule-list'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReservationSchedule.objects.count(), 2)

    def test_admin_retrieve_schedule(self):
        response = self.admin_client.get(
            reverse('reserve:admin-reservation-schedule-detail', kwargs={'id': self.schedule.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.schedule.id))

    def test_admin_update_schedule(self):
        data = {
            'operator_id': self.operator_user.id,
            'date': (timezone.now().date() + timedelta(days=2)).isoformat(),
            'period': 'AFTERNOON',
            'time_slot': '15-17',
            'duration': 45
        }
        response = self.admin_client.put(
            reverse('reserve:admin-reservation-schedule-detail', kwargs={'id': self.schedule.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_list_schedules(self):
        response = self.admin_client.get(reverse('reserve:admin-reservation-schedule-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ReservationSchedule User Tests
    def test_customer_list_schedules(self):
        response = self.customer_client.get(reverse('reserve:reservation-schedule-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_customer_retrieve_schedule(self):
        response = self.customer_client.get(
            reverse('reserve:reservation-schedule-detail', kwargs={'id': self.schedule.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.schedule.id))

    def test_customer_available_schedules(self):
        response = self.customer_client.get(
            reverse('reserve:reservation-schedule-available'), {'date': timezone.now().date().isoformat()}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_customer_available_schedules_missing_date(self):
        response = self.customer_client.get(reverse('reserve:reservation-schedule-available'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Reservation Admin Tests
    def test_admin_create_reservation(self):
        data = {
            'user_id': self.customer_user.id,
            'schedule_id': self.schedule.id,
            'laser_area_id': self.laser_area.id,
            'laser_area_schedules': [self.laser_schedule.id],
            'session_number': 2,
            'total_price': 1500.00,
            'final_amount': 1500.00,
            'is_paid': False
        }
        response = self.admin_client.post(reverse('reserve:admin-reservation-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 2)

    def test_admin_retrieve_reservation(self):
        response = self.admin_client.get(
            reverse('reserve:admin-reservation-detail', kwargs={'id': self.reservation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.reservation.id))

    def test_admin_update_reservation(self):
        data = {
            'user_id': self.customer_user.id,
            'schedule_id': self.schedule.id,
            'laser_area': self.laser_area.id,
            'laser_area_schedules': [self.laser_schedule.id],
            'session_number': 1,
            'total_price': 2000.00,
            'final_amount': 2000.00,
            'is_paid': True
        }
        response = self.admin_client.put(
            reverse('reserve:admin-reservation-detail', kwargs={'id': self.reservation.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation.refresh_from_db()
        self.assertTrue(self.reservation.is_paid)

    def test_admin_list_reservations(self):
        response = self.admin_client.get(reverse('reserve:admin-reservation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_unpaid_reservations(self):
        response = self.admin_client.get(reverse('reserve:admin-reservation-unpaid'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Reservation Customer Tests
    def test_customer_create_reservation(self):
        data = {
            'user_id': self.customer_user.id,
            'schedule_id': self.schedule.id,
            'laser_area_id': self.laser_area.id,
            'laser_area_schedules': [self.laser_schedule.id],
            'session_number': 2,
            'total_price': 1000.00,
            'final_amount': 1000.00
        }
        response = self.customer_client.post(reverse('reserve:user-reservation-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 2)

    def test_customer_retrieve_own_reservation(self):
        response = self.customer_client.get(
            reverse('reserve:user-reservation-detail', kwargs={'id': self.reservation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.reservation.id))

    def test_customer_retrieve_other_reservation(self):
        other_reservation = Reservation.objects.create(
            user=self.operator_user, schedule=self.schedule, laser_area=self.laser_area,
            session_number=1, total_price=1000.00, final_amount=1000.00
        )
        other_reservation.laser_area_schedules.add(self.laser_schedule)
        response = self.customer_client.get(
            reverse('reserve:user-reservation-detail', kwargs={'id': other_reservation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_list_own_reservations(self):
        response = self.customer_client.get(reverse('reserve:user-reservation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Reservation Operator Tests
    def test_operator_retrieve_assigned_reservation(self):
        response = self.operator_client.get(
            reverse('reserve:operator-reservation-detail', kwargs={'id': self.reservation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.reservation.id))

    def test_operator_retrieve_unassigned_reservation(self):
        other_schedule = ReservationSchedule.objects.create(
            operator=self.customer_user, date=timezone.now().date(),
            period='AFTERNOON', time_slot='15-17', duration=30
        )
        other_reservation = Reservation.objects.create(
            user=self.customer_user, schedule=other_schedule, laser_area=self.laser_area,
            session_number=1, total_price=1000.00, final_amount=1000.00
        )
        other_reservation.laser_area_schedules.add(self.laser_schedule)
        response = self.operator_client.get(
            reverse('reserve:operator-reservation-detail', kwargs={'id': other_reservation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_operator_list_assigned_reservations(self):
        response = self.operator_client.get(reverse('reserve:operator-reservation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_operator_mark_complete(self):
        response = self.operator_client.patch(
            reverse('reserve:operator-reservation-mark-complete', kwargs={'id': self.reservation.id}),
            data={'is_charged': True}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation.refresh_from_db()
        self.assertTrue(response.json()['is_charged'])

    # PreReservation Admin Tests
    def test_admin_create_pre_reservation(self):
        data = {
            'user_id': self.customer_user.id,
            'laser_area_schedule_id': self.laser_schedule.id,
            'session_count': 5,
            'last_session_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }
        response = self.admin_client.post(reverse('reserve:admin-pre-reservation-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PreReservation.objects.count(), 2)

    def test_admin_retrieve_pre_reservation(self):
        response = self.admin_client.get(
            reverse('reserve:admin-pre-reservation-detail', kwargs={'id': self.pre_reservation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.pre_reservation.id))

    def test_admin_update_pre_reservation(self):
        data = {
            'user_id': self.customer_user.id,
            'laser_area_schedule_id': self.laser_schedule.id,
            'session_count': 8,
            'last_session_date': (timezone.now().date() + timedelta(days=2)).isoformat()
        }
        response = self.admin_client.put(
            reverse('reserve:admin-pre-reservation-detail', kwargs={'id': self.pre_reservation.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_list_pre_reservations(self):
        response = self.admin_client.get(reverse('reserve:admin-pre-reservation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # PreReservation User Tests
    def test_customer_retrieve_own_pre_reservation(self):
        response = self.customer_client.get(
            reverse('reserve:pre-reservation-detail', kwargs={'id': self.pre_reservation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.pre_reservation.id))

    def test_customer_retrieve_other_pre_reservation(self):
        other_pre_reservation = PreReservation.objects.create(
            user=self.operator_user, laser_area_schedule=self.laser_schedule,
            session_count=5, last_session_date=timezone.now().date()
        )
        response = self.customer_client.get(
            reverse('reserve:pre-reservation-detail', kwargs={'id': other_pre_reservation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_list_own_pre_reservations(self):
        response = self.customer_client.get(reverse('reserve:pre-reservation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_access(self):
        response = self.unauthenticated_client.get(reverse('reserve:reservation-schedule-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)