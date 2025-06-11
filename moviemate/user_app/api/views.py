from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from user_app.api.serializers import RegistrationUserSerializer
# from user_app import models


class RegistrationView(APIView):
    """
    View to handle user registration.
    """
    
    def post(self, request):
        serializer = RegistrationUserSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            user = serializer.save()
            data['username'] = user.username
            data['email'] = user.email
            data['message'] = 'User registered successfully'
            # Model token DRF default
            # token = Token.objects.get(user=user).key #use the function create_auth_token from user model, se recomienda esta opcion para encapsular la logica de creacion del token
            # token = Token.objects.create(user=user).key  # use directly create the token from the token model
            # data['token'] = token
            
            # Token JWT
            token = RefreshToken.for_user(user)
            data['token'] = {
                'refresh': str(token),
                'access': str(token.access_token)
            }
            
            return Response(data, status=status.HTTP_201_CREATED)
            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LogoutView(APIView):
    """
    View to handle user logout.
    """
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)    
    
    
    
