from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework_simplejwt.views import (
                                            TokenObtainPairView,
                                            TokenRefreshView,
                                        )

from user_app.api.views import RegistrationView, LogoutView




urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),  # Endpoint for user registration
    # Endpoint for user authentication using DRF default token authentication
    #path('login/', ObtainAuthToken.as_view(), name='login'),  # Endpoint for user login
    #path('logout/', LogoutView.as_view(), name='logout'),  # Endpoint for user logout
    # Endpoint for user authentication using JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
