from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

CustomUser = get_user_model()

class UserAPITests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass',
            first_name='AdminFirst',
            last_name='AdminLast'
        )
        self.admin_token, _ = Token.objects.get_or_create(user=self.admin_user)
        
        self.non_admin_user = CustomUser.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass',
            role='patient',
            first_name='UserFirst',
            last_name='UserLast'
        )
        self.non_admin_token, _ = Token.objects.get_or_create(user=self.non_admin_user)
        
        self.login_url = reverse('login')
        self.user_list_url = reverse('user-list')
        self.user_detail_url = lambda user_id: reverse('user-detail', args=[user_id])
        
    def test_login_success(self):
        response = self.client.post(self.login_url, {'username': 'admin', 'password': 'adminpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {'username': 'nonexistentuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Invalid credentials')

    def test_user_list_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 

    def test_user_list_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.non_admin_token.key)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_create_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(self.user_list_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'role': 'doctor',
            'specialization': 'Neurology',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 3)  

    def test_user_create_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.non_admin_token.key)
        response = self.client.post(self.user_list_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'role': 'doctor',
            'specialization': 'Neurology',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(self.user_detail_url(self.non_admin_user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.non_admin_user.username)
        self.assertEqual(response.data['first_name'], self.non_admin_user.first_name)
        self.assertEqual(response.data['last_name'], self.non_admin_user.last_name)

    def test_user_detail_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.non_admin_token.key)
        response = self.client.get(self.user_detail_url(self.admin_user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.put(self.user_detail_url(self.non_admin_user.id), {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'password': 'newpassword',
            'role': 'doctor',
            'specialization': 'Cardiology',
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')
        self.assertEqual(response.data['specialization'], 'Cardiology')
        self.assertEqual(response.data['first_name'], 'UpdatedFirst')
        self.assertEqual(response.data['last_name'], 'UpdatedLast')

    def test_user_update_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.non_admin_token.key)
        
        response = self.client.put(self.user_detail_url(self.non_admin_user.id), {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'password': 'newpassword',
            'role': 'doctor',  
            'specialization': 'Cardiology',
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast'
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.non_admin_user.refresh_from_db()
        self.assertEqual(self.non_admin_user.username, 'user')  
        self.assertEqual(self.non_admin_user.email, 'user@example.com')  
        self.assertEqual(self.non_admin_user.first_name, 'UserFirst')  
        self.assertEqual(self.non_admin_user.last_name, 'UserLast')  



    def test_user_delete_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        user_to_delete = CustomUser.objects.create_user(
            username='deletableuser',
            email='delete@example.com',
            password='deletepass',
            role='doctor',
            first_name='DeleteFirst',
            last_name='DeleteLast'
        )
        response = self.client.delete(self.user_detail_url(user_to_delete.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 2)  

    def test_user_delete_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.non_admin_token.key)
        
        user_to_delete = CustomUser.objects.create_user(
            username='deletableuser',
            email='delete@example.com',
            password='deletepass',
            role='doctor',
            first_name='DeleteFirst',
            last_name='DeleteLast'
        )
        
        response = self.client.delete(self.user_detail_url(user_to_delete.id))
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.assertTrue(CustomUser.objects.filter(id=user_to_delete.id).exists())