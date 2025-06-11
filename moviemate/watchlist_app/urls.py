"""
    URLs for the watchlist application in pure DJANGO (Not used here in DRF).
"""

from django.urls import path

from watchlist_app.views import movie_list, movie_detail

urlpatterns = [
    path('list/', movie_list, name='movie-list'), #path espera tener una vista
    path('detail/<int:pk>/', movie_detail, name='movie-detail'),  # <int:pk> es un parámetro de la URL que se pasará a la vista
]