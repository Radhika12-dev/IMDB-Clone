from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class RegisterUserTestCase(APITestCase):
    def test_register_user(self):
        data = {
            "username" : "testuser",
            "email" : "testuser@example.com",
            "password" : "testpass123",
            "password2" : "testpass123"
        }
        #reverse is used to get the URL of the view by its name.
        # The name of the view is 'api_register' as defined in urls.py
        response = self.client.post(reverse('api_register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogoutUserTestCase(APITestCase):

    #For login and logout testing we need to create a user first which is done by overriding the setUp method.
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user.save()
        # Creating a token for the user.
        self.token = Token.objects.create(user=self.user)
    
    def test_login_user(self):
        data = {
            "username" : "testuser",
            "password" : "testpass123"
        }
        response = self.client.post(reverse('api_login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_logout_user(self):
        # First we need to get the token for the user
        self.token = Token.objects.get(user__username='testuser')

        #Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('api_logout'), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 