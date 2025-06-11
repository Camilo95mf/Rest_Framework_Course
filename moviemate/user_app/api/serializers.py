from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class RegistrationUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already exists.")]
    )
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    # Se recomienda sobreescribir el método create en lugar de save para crear una instancia del modelo
    # y devolverla, ya que el método save se utiliza para guardar una instancia existente del modelo.
    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        # Remove the password2 field from validated_data
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user