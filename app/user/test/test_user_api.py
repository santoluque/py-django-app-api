from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
'''CREATION URLS '''
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class publicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_create_user_success(self):
        payload = {
            'email': 'userapi@email.com',
            'password': 'abcpass',
            'name': 'User API'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        
    def test_user_with_email_exists_error(self):
        payload = {
            'email': 'usertwo@mail.com',
            'password': 'Clave1234',
            'name': 'Test User two',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_too_short_error(self):
        payload = {
            'email': 'userthree@mail.com',
            'password': 'cl',
            'name': 'User three',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        
        self.assertFalse(user_exists)
    
    
    def test_create_token_for_user(self):
        user_details = {
            'name': 'Test Name Token',
            'email': 'testoken@mail.com',
            'password': 'Clave1234',
        }
        create_user(**user_details)
        
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)
        print(res.data)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_create_token_bad_credentials(self):
        create_user(email='baduser@mail.com', password='badpass')
        payload = {'email': 'badcre@gmail.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_create_token_blank_password(self):
       
        payload = {'email': 'blank@gmail.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        

class PrivateUserApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email='userpu@mail.com',
            password='Clave12345',
            name='User private',            
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'name': self.user.name,
            'email': self.user.email,
        })
        
    ''' def test_post_me_not_allowed(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) '''
    
    def test_update_user_profile(self):
        payload = {'name': 'update name', 'password': 'newpassword2024'}
        res = self.client.patch(ME_URL, payload)
        
        self.user.refresh_from_db()
        
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    
    
        
    
        
