from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

# from rest_framework_simplejwt.tokens import RefreshToken


class RegisterTetsCase(APITestCase):
    """
    Test case for user registration.
    """

    def test_register(self):
        """
        Test user registration with valid data.
        """
        # url = reverse('user:register')
        # Los datos que se envian en el body, no seran guardados en la base de datos
        data = {
            'username': 'testuser',
            'email': 'test@mail.com',
            'password': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(reverse('register'), data, format='json') #La funcion reverse permite obtener la url de la vista por su nombre, en este caso 'register' que es el nombre de la vista de registro definida en user_app/api/urls.py
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Verifica que el codigo de respuesta sea 201 Created
        
        
class LoginRefreshTestCase(APITestCase):
    """
    Test case for user login and logout.
    """

    # en este metodo se crea un usuario para poder hacer login y logout
    # en general se usa el metodo setUp de la clase TestCase para crear los datos necesarios para las pruebas
    def setUp(self):
        """
        Set up a user for testing login and logout.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
    def test_login(self):
        """
        Test user login with valid credentials.
        """
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('token_obtain_pair'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data) # Check if access token is returned in the response
        self.assertIn('refresh', response.data) # Check if refresh token is returned in the response
        
    def test_refresh(self):
        """
        Test token refresh.
        """
        token = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        }, format='json').data['refresh'] # Get the refresh token from the login response
        
        response = self.client.post(reverse('token_refresh'), {'refresh': token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data) # Check if new access token is returned in the response
        
        
        
        

