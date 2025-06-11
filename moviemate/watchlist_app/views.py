"""
    Views for the watchlist application in pure DJANGO (Not used with DRF).
"""

from django.shortcuts import render
from django.http import JsonResponse
# from django.forms.models import model_to_dict

from watchlist_app.models import Movie


def movie_list(request):
    movies = Movie.objects.all()
    return JsonResponse(list(movies.values()), safe=False)  # Convert queryset to list of dictionaries

def movie_detail(request, pk):
    movie = Movie.objects.filter(pk=pk).values("name", "description").first()  # Use filter and first to avoid DoesNotExist exception
    print(movie)
    print()
    return JsonResponse(dict(movie), safe=False)