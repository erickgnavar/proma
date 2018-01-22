"""proma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path

from proma.views import HomeView

admin.site.site_title = 'Proma'
admin.site.site_header = 'Proma'

urlpatterns = [
    path('super/', admin.site.urls),
    path('', include('proma.users.urls', namespace='auth')),
    path('', include('proma.clients.urls', namespace='clients')),
    path('', include('proma.projects.urls', namespace='projects')),
    path('', HomeView.as_view(), name='home'),
]
