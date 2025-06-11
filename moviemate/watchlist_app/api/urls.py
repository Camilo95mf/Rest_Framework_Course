from django.urls import path, include

from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import (WatchListView, WatchDetailView, 
                                     StreamPlatformListView, StreamPlatformDetailView, 
                                     ReviewListView, ReviewDetailView,
                                     ReviewCreateView, StreamPlatformView,
                                     UserReviewView, WatchListFilterView)




router = DefaultRouter()
router.register('stream', StreamPlatformView, basename='streamplatform')  # Register the StreamPlatformView with the router

urlpatterns = [
    # function based views
    # path('list/', movie_list, name='movie-list'), #path espera tener una vista
    # path('detail/<int:pk>/', movie_detail, name='movie-detail'),  # <int:pk> es un parámetro de la URL que se pasará a la vista
    # class based views
    # Para los names de las vistas, se recomienda usar el formato 'modelname-<action>' para evitar conflictos con otras aplicaciones
    path('list/', WatchListView.as_view(), name='watchlist-list'), #path espera tener una vista
    path('<int:pk>/', WatchDetailView.as_view(), name='watchlist-detail'),  # <int:pk> es un parámetro de la URL que se pasará a la vista
    path('list-filter/', WatchListFilterView.as_view(), name='watchlist-filter'),  # Filter view for watchlist
    
    # path('stream/', StreamPlatformListView.as_view(), name='StreamPlatform-list'),
    # path('stream/<int:pk>/', StreamPlatformDetailView.as_view(), name='streamplatform-detail'),
    path('', include(router.urls)),  # Include the router URLs for StreamPlatformView using rest_framework's DefaultRouter
    
    # path('review/', ReviewListView.as_view(), name='review-list'),
    # path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('<int:pk>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('<int:pk>/review-create/', ReviewCreateView.as_view(), name='review-create'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    # User-specific review detail view using path parameter
    # path('reviews/<str:username>/', UserReviewView.as_view(), name='user-review-detail'),
    
    # user User-specific detail view using query parameter
    path('reviews/', UserReviewView.as_view(), name='user-review-detail'),
    
]