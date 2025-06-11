from rest_framework import serializers

from watchlist_app.models import WatchList, StreamPlatform, Review



# -------------- serializers.modelserializer ---------------

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)  # Use StringRelatedField to return the string representation of the related user 
    
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ['watchlist']  # Exclude the WatchList field to avoid circular reference

class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)  # Nested serializer to include related reviews
    
    # How to add a custom field to the serializer
    # custom_field = serializers.SerializerMethodField()
    # platform_name = serializers.StringRelatedField(read_only=True)  # Use StringRelatedField to return the string representation of the related platform
    platform_name = serializers.CharField(source='platform.name', read_only=True)  # Use CharField to return the name of the related platform
    len_title = serializers.SerializerMethodField()  # Custom field to get the length of the name
    
    class Meta:
        model = WatchList
        fields = '__all__'  # Incluye todos los campos del modelo Movie en la serialización
        # También se puede especificar una lista de campos específicos o excluir algunos campos
        # fields = ['id', 'name', 'description']  # Especifica los campos del modelo que se incluirán en la serialización
        # exclude = ['active']

    def get_len_title(self, obj):
        """
        Custom method to return the length of the name field.
        """
        return len(obj.title)

    # Se pueden añadir validaciones personalizadas para los campos del modelo
    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError("The name and description cannot be the same.")
        else:
            return data
    
    def validate_title(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("The name must be at least 4 characters long.")
        else:
            return value   
        
        
# class StreamPlatformSerializer(serializers.ModelSerializer):
class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer): # HyperlinkedModelSerializer represents relations as hyperlinks instead of primary keys
    
    watchlist = WatchListSerializer(many=True, read_only=True)  # Nested serializer to include related watchlist items return all fields
    # watchlist = serializers.StringRelatedField(many=True, read_only=True)  # Use StringRelatedField to return the string representation of the related watchlist items
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # PrimaryKeyRelatedField to return the primary keys of the related watchlist items
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie-detail',  # The name of the view that will handle the detail view of the watchlist items, the view_name should match the name defined in the urls.py
    # )
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'  # Include all fields from the StreamPlatform model
        # fields = ['id', 'name', 'about', 'website']  # Specify the fields to include in the serialization
        # exclude = ['created']  # Exclude the created field from the serialization



# -------------- serializers.serializer ---------------

# def name_length(value):
#     """
#     Custom validator to check if the name is at least 4 characters long.
#     """
#     if len(value) < 4:
#         raise serializers.ValidationError("The name must be at least 4 characters long...")
#     return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=50, validators=[name_length])  # Custom validator for name length
#     description = serializers.CharField(max_length=200)
#     active = serializers.BooleanField(default=True)
    
#     def create(self, validated_data):
#         """
#         Create and return a new `Movie` instance, given the validated data.
#         """
#         Movie.objects.create(**validated_data)
#         return validated_data
    
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Movie` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     # custom validation for the entire serializer
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("The name and description cannot be the same.")
#         else:
#             return data
    
    #Field-level validation (custom validation for individual fields)
    # def validate_name(self, value):
    #     if len(value) < 4:
    #         raise serializers.ValidationError("The name must be at least 4 characters long.")
    #     else:
    #         return value    
    