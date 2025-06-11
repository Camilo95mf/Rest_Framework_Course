from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.validators import ValidationError
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView # Cambia api_view por APIView para usar clases en lugar de funciones
from rest_framework import generics  # Importa generics si deseas usar vistas genéricas
from rest_framework import viewsets  # Importa viewsets si deseas usar vistas basadas en conjuntos de vistas
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly  # Importa permisos para controlar el acceso a las vistas
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle  # Importa throttling para limitar la tasa de solicitudes
from rest_framework import filters

#Django-filter
from django_filters.rest_framework import DjangoFilterBackend  # Importa DjangoFilterBackend para filtrar resultados en las vistas

from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (WatchListSerializer, StreamPlatformSerializer, 
                                           ReviewSerializer)
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly  # Importa permisos personalizados
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from watchlist_app.api.pagination import WatchListPagination  # Importa la paginación personalizada

# --------------- views basadas en clases ---------------

#  ********* Views usando Django Rest Framework's viewsets ********

class StreamPlatformView(viewsets.ModelViewSet): # Con este tipo de vista, puedes manejar las operaciones CRUD de manera mucho mas sencilla
    """
    view to handle the streaming plaforms using ModelViewSet.
    """
    permission_classes = [IsAdminOrReadOnly]  # Permite que solo los administradores puedan modificar o eliminar objetos, los usuarios autenticados pueden ver los detalles
    queryset = StreamPlatform.objects.all()  # Define el queryset para obtener todos los objetos StreamPlatform
    serializer_class = StreamPlatformSerializer  # Define el serializer a usar
    


# class StreamPlatformView(viewsets.ViewSet): # Con este tipo de vista, puedes manejar las operaciones CRUD de manera más sencilla y organizada y mas o menos perzonalizada.
#     """
#     view to handle the streaming plaforms using viewset.
#     """
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True, context={'request': request}) #context is for including the request in the hyperlinks of HyperlinkedModelSerializer
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist, context={'request': request})
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         watchlist.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    


#  ********* Views usando Django Rest Framework's generics views *********

class WatchListFilterView(generics.ListCreateAPIView):
    queryset = WatchList.objects.all()  # Define el queryset para obtener todos los objetos WatchList
    serializer_class = WatchListSerializer  # Define el serializer a usar
    # permission_classes = [IsAuthenticated]  # Permite que solo los usuarios autenticados puedan acceder a esta vista
    # throttle_classes = [ReviewListThrottle]
    filter_backends = [filters.SearchFilter]  # Permite buscar en los resultados usando SearchFilter
    search_fields = ['title','platform__name']  # Permite buscar por el campo title y por el nombre de la plataforma asociada
    ordering_fields = ['avg_rating']  # Permite ordenar los resultados por avg_rating y number_ratings
    pagination_class = WatchListPagination
    
    

class UserReviewView(generics.ListAPIView):
    """
    View to handle the list of reviews created by a specific user.
    """
    serializer_class = ReviewSerializer  # Define el serializer a usar
    # permission_classes = [IsAuthenticated]  # Permite que solo los usuarios autenticados puedan acceder a esta vista
    # throttle_classes = [ReviewListThrottle]  # Limita la tasa de solicitudes para la lista de reviews
    
    # Se usa path parameters para obtener el username del usuario de la URL
    # def get_queryset(self):
    #     username = self.kwargs.get('username')  # Obtiene el pk de la URL
    #     return Review.objects.filter(review_user__username=username)   # Filtra las reviews por el usuario
    
    def get_queryset(self):
        username = self.request.query_params.get('username')  # Obtiene el username de los parámetros de la consulta
        if username:
            return Review.objects.filter(review_user__username=username)
        else:
            return Review.objects.all()
    

class ReviewCreateView(generics.CreateAPIView):
    """
    View to handle the creation of reviews.
    """
    queryset = Review.objects.all()  # Define el queryset para obtener todos los objetos Review
    serializer_class = ReviewSerializer  # Define el serializer a usar
    throttle_classes = [ReviewCreateThrottle]  # Limita la tasa de solicitudes para la creación de reviews
    
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)  # Obtiene el objeto WatchList asociado al pk
        
        user = self.request.user  # Obtiene el usuario que está haciendo la solicitud
        review_queryset = Review.objects.filter(watchlist=movie, review_user=user)  # Filtra las reviews por el watchlist y el usuario
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie.")
        
        if movie.number_ratings == 0:
            movie.avg_rating = serializer.validated_data['rating'] # Si es la primera review, establece el avg_rating al rating de la nueva review
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / (movie.number_ratings + 1)
            
        movie.number_ratings += 1  # Incrementa el número de ratings
        
        movie.save()  # Guarda el objeto WatchList actualizado
        
        serializer.save(watchlist=movie, review_user=user)  # Guarda la nueva review asociada al watchlist

class ReviewListView(generics.ListAPIView):
    """
    View to handle the list and creation of reviews.
    """
    # Para obtener solo las reviews de una pelicula especifica debemos hacer override del método get_queryset
    # queryset = Review.objects.all()  # Define el queryset para obtener todos los objetos Review
    serializer_class = ReviewSerializer  # Define el serializer a usar
    # permission_classes = [IsAuthenticated]  # Permite que solo los usuarios autenticados puedan acceder a esta vista
    # throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]  # Permite filtrar los resultados usando DjangoFilterBackend
    filterset_fields = ['review_user__username','active','rating']  # Permite filtrar las reviews por el campo rating
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')  # Obtiene el pk de la URL
        return Review.objects.filter(watchlist=pk)  # Filtra las reviews por el watchlist asociado al pk
    
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to handle the details of a specific review.
    """
    queryset = Review.objects.all()  # Define el queryset para obtener todos los objetos Review
    serializer_class = ReviewSerializer  # Define el serializer a usar
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]  # Limita la tasa de solicitudes para usuarios autenticados y anónimos
    throttle_scope = 'review-detail'  # Define el scope para la tasa de solicitudes


#  ********* Views usando Django Rest Framework's mixins y generics *********

# class ReviewDetailView(generics.mixins.RetrieveModelMixin,
#                        generics.mixins.UpdateModelMixin,
#                        generics.mixins.DestroyModelMixin,
#                        generics.GenericAPIView):
#     """
#     View to handle the details of a specific review.
#     """
#     queryset = Review.objects.all()  # Define el queryset para obtener todos los objetos WatchList
#     serializer_class = ReviewSerializer  # Define el serializer a usar
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewListView(generics.mixins.ListModelMixin,
#                      generics.mixins.CreateModelMixin,
#                      generics.GenericAPIView):
#     """
#     View to handle the list of reviews.
#     """
    
#     queryset = Review.objects.all()  # Define el queryset para obtener todos los objetos WatchList
#     serializer_class = ReviewSerializer  # Define el serializer a usar
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)  # Llama al método list para manejar la solicitud GET
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)  # Llama al método create para manejar la solicitud POST


#  ********* Views usando estandar classed based views APIVIEW *********

class WatchListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)  # Serializa la lista de películas
        return Response(serializer.data)  # Devuelve la respuesta con los datos serializados
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():  # Verifica si los datos enviados son válidos
            serializer.save()  # Guarda el nuevo objeto Movie en la base de datos
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Devuelve la respuesta con los datos serializados y un estado 201 (creado)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]  # Permite que solo los administradores puedan modificar o eliminar objetos, los usuarios autenticados pueden ver los detalles
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)  # Obtiene el objeto Movie por su clave primaria (pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un error si la película no existe

        serializer = WatchListSerializer(movie)  # Serializa el objeto Movie
        return Response(serializer.data)  # Devuelve la respuesta con los datos serializados
    
    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie, data=request.data) # Serializa el objeto con la instancia existente y los datos de la solicitud
        if serializer.is_valid():
            serializer.save()  # Actualiza el objeto Movie con los datos validados
            return Response(serializer.data, status=status.HTTP_200_OK)  # Devuelve la respuesta con los datos actualizados y un estado 200 (OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)  # Obtiene el objeto Movie por su clave primaria (pk)
            movie.delete()  # Elimina el objeto Movie de la base de datos
            return Response(status=status.HTTP_204_NO_CONTENT)  # Devuelve una respuesta vacía con un estado 204 (No Content)
        except WatchList.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un error si la película no existe
        
        
        
class StreamPlatformListView(APIView):
    """
    View to handle the streaming plaforms.
    """
    
    def get(self, request):
        platforms = StreamPlatform.objects.all()  # Obtiene todos los objetos StreamPlatform de la base de datos
        serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})  # Serializa la lista de StreamPlatform, context es para incluir el request en los enlaces de HyperlinkedRelatedField
        return Response(serializer.data, status=status.HTTP_200_OK)  # Devuelve la respuesta con los datos serializados
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():  # Verifica si los datos enviados son válidos
            serializer.save()  # Guarda el nuevo objeto StreamPlatform en la base de datos
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Devuelve la respuesta con los datos serializados y un estado 201 (creado)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class StreamPlatformDetailView(APIView):
    """
    View to handle the details of a specific streaming plaform.
    """
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un error si la StreamPlatform no existe

        serializer = StreamPlatformSerializer(platform, context={'request': request})  # Serializa el objeto StreamPlatform
        return Response(serializer.data, status=status.HTTP_200_OK)  # Devuelve la respuesta con los datos serializados
    
    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'StreamPlatform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, data=request.data) # Serializa el objeto con la instancia existente y los datos de la solicitud
        if serializer.is_valid():
            serializer.save()  # Actualiza el objeto StreamPlatform con los datos validados
            return Response(serializer.data, status=status.HTTP_200_OK)  # Devuelve la respuesta con los datos actualizados y un estado 200 (OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)  # Obtiene el objeto StreamPlatform por su clave primaria (pk)
            platform.delete()  # Elimina el objeto StreamPlatform de la base de datos
            return Response(status=status.HTTP_204_NO_CONTENT)  # Devuelve una respuesta vacía con un estado 204 (No Content)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'StreamPlatform not found'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un error si la StreamPlatform no existe
    
    
    
    
    
    
        
# --------------- views basas en funciones ---------------

# @api_view(['GET', 'POST'])  # Permite manejar solicitudes GET y POST
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()  # Obtiene todos los objetos Movie de la base de datos
#         serializer = MovieSerializer(movies, many=True)  # Serializa la lista de películas
#         return Response(serializer.data)  # Devuelve la respuesta con los datos serializados

#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():  # Verifica si los datos enviados son válidos
#             serializer.save()  # Guarda el nuevo objeto Movie en la base de datos
#             return Response(serializer.data, status=status.HTTP_201_CREATED)  # Devuelve la respuesta con los datos serializados y un estado 201 (creado)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Devuelve un error si los datos no son válidos

# @api_view(['GET', 'PUT', 'DELETE'])  # Permite manejar solicitudes GET, PUT y DELETE
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)  # Obtiene el objeto Movie por su clave primaria (pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un error si la película no existe

#         serializer = MovieSerializer(movie)  # Serializa el objeto Movie
#         return Response(serializer.data)  # Devuelve la respuesta con los datos serializados
    
#     if request.method == 'PUT':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie, data=request.data) # Serializa el objeto con la instancia existente y los datos de la solicitud
#         if serializer.is_valid():
#             serializer.save()  # Actualiza el objeto Movie con los datos validados
#             return Response(serializer.data, status=status.HTTP_200_OK)  # Devuelve la respuesta con los datos actualizados y un estado 200 (OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method == 'DELETE':
#         try:
#             movie = Movie.objects.get(pk=pk)  # Obtiene el objeto Movie por su clave primaria (pk)
#             movie.delete()  # Elimina el objeto Movie de la base de datos
#             return Response(status=status.HTTP_204_NO_CONTENT)  # Devuelve una respuesta vacía con un estado 204 (No Content)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un error si la película no existe
    