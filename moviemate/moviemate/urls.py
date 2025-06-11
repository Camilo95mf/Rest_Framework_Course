"""
URL configuration for moviemate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from watchlist_app import urls as watchlist_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watchlist/', include('watchlist_app.api.urls')), # Para agregar una url de otra app (modulo), se usa include que espera un archivo urls.py dentro de la app pasar como str
    # path('api-auth/', include('rest_framework.urls')),  # Para la autenticación de la API de Django REST Framework (temporal para pruebas, no es recomendable usarlo en producción)
    path('account/', include('user_app.api.urls')),  # Include the user app URLs for user management
]
