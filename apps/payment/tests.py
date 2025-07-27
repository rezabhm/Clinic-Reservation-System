from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
from .models import Payment, DiscountCode
from apps.core.models import CustomUser, UserRole
from apps.lazer_area.models import LaserArea, LaserAreaSchedule
from ..reserve.models import Reservation, ReservationSchedule
from ..reserve.serializers.reserve import ReservationSerializer


class PaymentViewsTestCase(TestCase):
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
        self.schedule = ReservationSchedule.objects.create(
            operator=self.operator_user, date=timezone.now().date(),
            period='MORNING', time_slot='8-10',
        )
        self.laser_schedule = LaserAreaSchedule.objects.create(
            laser_area=self.laser_area, start_time=timezone.now() + timedelta(hours=1),
            price=100000.00
        )
        self.reservation = Reservation.objects.create(
            user=self.customer_user, schedule=self.schedule, laser_area=self.laser_area, is_paid=False,
            total_price=1000.00, final_amount=1000.00, session_number=1452
        )
        self.reservation.save()
        self.reservation.laser_area_schedules.add(self.laser_schedule)
        self.payment = Payment.objects.create(
            user=self.customer_user, reservation=self.reservation, amount=100.00, status='PENDING', paypal_transaction_id='111111'
        )
        self.discount_code = DiscountCode.objects.create(
            code='TESTCODE', amount=10.00, valid_until=timezone.now() + timedelta(days=1), is_used=False
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

    # Payment Admin Tests
    def test_admin_create_payment(self):
        reservation_serializer = ReservationSerializer(self.reservation, many=False)
        data = {
            'user_id': self.customer_user.id,
            'laser_area_id': self.laser_area.id,
            'amount': 150.00,
            'reservation': reservation_serializer.data,
            'reservation_id': self.reservation.id,
            'status': 'PENDING',
            'paypal_transaction_id':'545151'
        }
        response = self.admin_client.post(reverse('payment:admin-payment-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 2)

    def test_admin_create_payment_invalid(self):
        data = {'user_id': self.customer_user.id, 'amount': -10.00}
        response = self.admin_client.post(reverse('payment:admin-payment-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_payment(self):
        response = self.admin_client.get(
            reverse('payment:admin-payment-detail', kwargs={'id': self.payment.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.payment.id))

    def test_admin_update_payment(self):
        reservation_serializer = ReservationSerializer(self.reservation, many=False)

        data = {
            'user_id': self.customer_user.id,
            'laser_area_id': self.laser_area.id,
            'amount': 200.00,
            'reservation': reservation_serializer.data,
            'reservation_id': self.reservation.id,
            'status': 'COMPLETED',
            'paypal_transaction_id': '545'

        }
        response = self.admin_client.put(
            reverse('payment:admin-payment-detail', kwargs={'id': self.payment.id}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'COMPLETED')

    def test_admin_list_payments(self):
        response = self.admin_client.get(reverse('payment:admin-payment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_pending_payments(self):
        response = self.admin_client.get(reverse('payment:admin-payment-pending'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Payment Customer Tests
    def test_customer_create_payment(self):
        reservation_serializer = ReservationSerializer(self.reservation, many=False)

        data = {
            'user_id': self.customer_user.id,
            'laser_area_id': self.laser_area.id,
            'amount': 150.00,
            'reservation': reservation_serializer.data,
            'reservation_id': self.reservation.id,
            'status': 'COMPLETED',
            'paypal_transaction_id': '545455'

        }
        response = self.customer_client.post(reverse('payment:payment-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 2)

    def test_customer_retrieve_own_payment(self):
        response = self.customer_client.get(
            reverse('payment:payment-detail', kwargs={'id': self.payment.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.payment.id))

    def test_customer_retrieve_other_payment(self):
        other_payment = Payment.objects.create(
            user=self.customer_user, reservation=self.reservation, amount=50.00, status='PENDING', paypal_transaction_id='124512'
        )
        response = self.customer_client.get(
            reverse('payment:payment-detail', kwargs={'id': other_payment.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_list_own_payments(self):
        response = self.customer_client.get(reverse('payment:payment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_operator_access_payment_view(self):
        response = self.operator_client.get(reverse('payment:payment-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # DiscountCode Admin Tests
    def test_admin_create_discount_code(self):
        data = {
            'code': 'NEWCOD',
            'discount_percentage': 20,
            'valid_until': (timezone.now() + timedelta(days=2)).isoformat(),
            'is_used': False,
            'amount':150.00
        }
        response = self.admin_client.post(reverse('payment:admin-discount-code-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DiscountCode.objects.count(), 2)

    def test_admin_retrieve_discount_code(self):
        response = self.admin_client.get(
            reverse('payment:admin-discount-code-detail', kwargs={'code': self.discount_code.code})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], self.discount_code.code)

    def test_admin_update_discount_code(self):
        data = {
            'code': 'UPDATEDCO',
            'discount_percentage': 15,
            'valid_until': (timezone.now() + timedelta(days=3)).isoformat(),
            'is_used': True,
            'amount': 15.00
        }
        response = self.admin_client.put(
            reverse('payment:admin-discount-code-detail', kwargs={'code': self.discount_code.code}), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.discount_code.refresh_from_db()
        self.assertEqual(self.discount_code.code, 'UPDATEDCO')

    def test_admin_list_discount_codes(self):
        response = self.admin_client.get(reverse('payment:admin-discount-code-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # DiscountCode User Tests
    def test_customer_list_discount_codes(self):
        response = self.customer_client.get(reverse('payment:discount-code-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_customer_retrieve_discount_code(self):
        response = self.customer_client.get(
            reverse('payment:discount-code-detail', kwargs={'code': self.discount_code.code})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], self.discount_code.code)

    def test_customer_retrieve_expired_discount_code(self):
        expired_code = DiscountCode.objects.create(
            code='EXPIREDCOD', amount=5.00, valid_until=timezone.now() + timedelta(days=1), is_used=False
        )
        response = self.customer_client.get(
            reverse('payment:discount-code-detail', kwargs={'code': expired_code.code})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_valid_discount_codes(self):
        response = self.customer_client.get(reverse('payment:discount-code-valid'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_access(self):
        response = self.unauthenticated_client.get(reverse('payment:payment-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)