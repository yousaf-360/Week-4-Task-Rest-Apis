from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from .models import Appointment
from django.contrib.auth import get_user_model

User = get_user_model()

class AppointmentAPITests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.doctor_user = User.objects.create_user(
            username='doctor',
            email='doctor@example.com',
            password='doctorpass',
            role='doctor'
        )
        self.patient_user = User.objects.create_user(
            username='patient',
            email='patient@example.com',
            password='patientpass',
            role='patient'
        )
        self.appointment = Appointment.objects.create(
            doctor=self.doctor_user,
            patient=self.patient_user,
            scheduled_at=timezone.now() + timezone.timedelta(days=1)
        )
        self.appointment_list_url = reverse('appointment-list')
        self.appointment_create_url = reverse('appointment-create')
        self.appointment_detail_url = reverse('appointment-detail', args=[self.appointment.id])
        self.appointment_summary_url = reverse('appointment-summary')

    def test_list_appointments_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.appointment_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_appointments_doctor(self):
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.get(self.appointment_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_appointments_forbidden(self):
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(self.appointment_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_appointment_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'doctor': self.doctor_user.id,
            'patient': self.patient_user.id,
            'scheduled_at': (timezone.now() + timezone.timedelta(days=2)).isoformat()
        }
        response = self.client.post(self.appointment_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)

    def test_create_appointment_forbidden(self):
        self.client.force_authenticate(user=self.doctor_user)
        data = {
            'doctor': self.doctor_user.id,
            'patient': self.patient_user.id,
            'scheduled_at': (timezone.now() + timezone.timedelta(days=2)).isoformat()
        }
        response = self.client.post(self.appointment_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_appointment_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.appointment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.appointment.id)

    def test_retrieve_appointment_doctor(self):
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.get(self.appointment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.appointment.id)

    def test_retrieve_appointment_forbidden(self):
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(self.appointment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_appointment_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'doctor': self.doctor_user.id,
            'patient': self.patient_user.id,
            'scheduled_at': (timezone.now() + timezone.timedelta(days=3)).isoformat()
        }
        response = self.client.put(self.appointment_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.doctor, self.doctor_user)
        self.assertEqual(self.appointment.patient, self.patient_user)
        self.assertEqual(self.appointment.scheduled_at.date(), (timezone.now() + timezone.timedelta(days=3)).date())

    def test_update_appointment_forbidden(self):
        self.client.force_authenticate(user=self.doctor_user)
        data = {
            'doctor': self.doctor_user.id,
            'patient': self.patient_user.id,
            'scheduled_at': (timezone.now() + timezone.timedelta(days=3)).isoformat()
        }
        response = self.client.put(self.appointment_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_appointment_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.appointment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_delete_appointment_forbidden(self):
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.delete(self.appointment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_summary_appointment_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.appointment_summary_url, {'start_date': timezone.now().date().isoformat()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_summary_appointment_forbidden(self):
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.get(self.appointment_summary_url, {'start_date': timezone.now().date().isoformat()})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
