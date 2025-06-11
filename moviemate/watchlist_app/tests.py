from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api import serializers

# Create your tests here.
class WatchListTests(APITestCase):
    def setUp(self):
        #se crea una plataforma y una watchlist para las pruebas
        # self.platform = StreamPlatform.objects.create(name='Netflix', about='Streaming service', website='https://www.netflix.com')
        self.platform = StreamPlatform.objects.create(
            name='Netflix',
            about='Streaming platform',
            website='https://www.netflix.com'
        )
        self.watchlist = WatchList.objects.create(title='Inception', storyline='A mind-bending thriller', platform=self.platform)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.jwt_token = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        }, format='json').data['access']
        # Se añade el token al header de la peticion para autenticar al usuario,
        # se hace en el setUp para que todas las pruebas tengan el token disponible
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_token)

    def test_watchlist_creation(self):
        data = {
            'title': 'The Matrix',
            'storyline': 'A hacker discovers the true nature of reality',
            'active': True,
            'platform': self.platform.id
        }
        response = self.client.post(reverse('watchlist-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('watchlist-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
    def test_watchlist_detail(self):
        response = self.client.get(reverse('watchlist-detail', args=[self.watchlist.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the response data contains the expected fields and values
        self.assertEqual(response.data['title'], self.watchlist.title)
        self.assertEqual(response.data['storyline'], self.watchlist.storyline)
        self.assertEqual(response.data['platform'], self.platform.id)
        
        
class StreamPlatformTests(APITestCase):
    def setUp(self):
        # Se crea un usuario para poder autenticar las peticiones
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.jwt_token = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        }, format='json').data['access']
        # Se añade el token al header de la peticion para autenticar al usuario,
        # se hace en el setUp para que todas las pruebas tengan el token disponible
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_token)
        
        # Se crea una plataforma de streaming para las pruebas
        self.platform = StreamPlatform.objects.create(name='Netflix', about='Streaming service', website='https://www.netflix.com')

    def test_streamplatform_creation(self):
        data = {
            'name': 'Hulu',
            'about': 'Streaming',
            'website': 'https://www.hulu.com',
            
        }
        # Here we use routing so the list method is standar following the DRF conventions
        # https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        response = self.client.post(reverse('streamplatform-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Check if the user is not allowed to create a StreamPlatform without permissions
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list) # Se verifica que el response sea una lista
        
    def test_streamplatform_detail(self):
        # Para enviar argumentos a la url, se usa el reverse con el nombre de la vista y los argumentos necesarios en args
        response = self.client.get(reverse('streamplatform-detail', args=[self.platform.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the response data contains the expected fields and values
        self.assertEqual(response.data['name'], self.platform.name)
        self.assertEqual(response.data['about'], self.platform.about)
        self.assertEqual(response.data['website'], self.platform.website)


class ReviewTests(APITestCase):
    def setUp(self):
        # Se crea un usuario para poder autenticar las peticiones
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.jwt_token = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        }, format='json').data['access']
        # Se añade el token al header de la peticion para autenticar al usuario,
        # se hace en el setUp para que todas las pruebas tengan el token disponible
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.jwt_token)
        
        # Se crea una plataforma de streaming y una watchlist para las pruebas
        self.platform = StreamPlatform.objects.create(name='Netflix', about='Streaming service', website='https://www.netflix.com')
        self.watchlist = WatchList.objects.create(title='Inception', storyline='A mind-bending thriller', platform=self.platform)
        
        self.review = Review.objects.create(review_user=self.user, rating=5, description='Great movie!', watchlist=self.watchlist)
        
    def test_review_creation(self):
        data = {
            'review_user': self.user.id,  # Use the user ID for the review
            'rating': 5,
            'description': 'Amazing movie!',
            'watchlist': self.watchlist.id
        }
        response = self.client.post(reverse('review-create', args=[self.watchlist.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) #User already has a review for this watchlist
        
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=[self.watchlist.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
    def test_review_detail(self):
        response = self.client.get(reverse('review-detail', args=[self.review.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the response data contains the expected fields and values
        self.assertEqual(response.data['rating'], self.review.rating)
        self.assertEqual(response.data['description'], self.review.description)
        
    def test_user_review_detail(self):
        # response = self.client.get(reverse('user-review-detail'), {'username': self.user.username}, format='json')
        response = self.client.get(f'/watchlist/reviews/?username={self.user.username}', format='json') #No se puede usar reverse ya que usamos query parameters
        self.assertEqual(response.status_code, status.HTTP_200_OK)