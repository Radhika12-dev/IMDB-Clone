from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# from imdb_app.api import serializers
from imdb_app.models import WatchList, Review, StreamingPlatform

class StreamingPlatformTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_streaming_platform(self):
        data = {
            'name': 'Netflix',
            'about': 'The world\'s largest and most popular streaming service.',
            'website': 'https://www.netflix.com/'
        }
        response = self.client.post(reverse('stream_platform'), data, format='json')
        #As admin can create a streaming platform, if a normal user tries to add a streaming platform, it should return 403 forbidden.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_streaming_platform(self):
        response = self.client.get(reverse('stream_platform'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class WatchListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.streaming_platform = StreamingPlatform.objects.create(
            name='Netflix',
            about='The world\'s largest and most popular streaming service.',
            website='https://www.netflix.com/'
        )

        self.watchlist_item = WatchList.objects.create(
            title='Inception',
            storyline='A thief who steals corporate secrets through the use of dream-sharing technology.',
            platform=self.streaming_platform,
            active=True
        )
        self.watchlist_item2 = WatchList.objects.create(
            title='The Matrix',
            storyline='A computer hacker learns from mysterious rebels about the true nature of his reality.',
            platform=self.streaming_platform,
            active=True
        )

    def test_create_watchlist_item(self):
        data = {
            'title': 'Inception',
            'storyline': 'A thief who steals corporate secrets through the use of dream-sharing technology.',
            'platform': self.streaming_platform.id,
            'active': True
        }
        response = self.client.post(reverse('movie_list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_watchlist_item(self):
        response = self.client.get(reverse('movie_detail', args=[self.watchlist_item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.streaming_platform = StreamingPlatform.objects.create(
            name='Netflix',
            about='The world\'s largest and most popular streaming service.',
            website='https://www.netflix.com/'
        )

        self.watchlist_item = WatchList.objects.create(
            title='Inception',
            storyline='A thief who steals corporate secrets through the use of dream-sharing technology.',
            platform=self.streaming_platform,
            active=True
        )
    
    def test_create_review(self):
        data = {
            'review_user': self.user.id,
            'rating': 5,
            'description': 'Amazing movie!',
            'watchlist': self.watchlist_item.id,
            'active': True
        }
        response = self.client.post(reverse('review_create', args=(self.watchlist_item.id,)), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_review_unauthorized_user(self):
        data = {
            # 'review_user': self.user,
            'rating': 5,
            'description': 'Amazing movie!',
            'watchlist': self.watchlist_item.id,
            'active': True
        }
       
        self.client.force_authenticate(user=None)  # Force unauthenticated user
        response = self.client.post(reverse('review_create', args=(self.watchlist_item.id,)), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
#use python.manage.py test to run the test cases.