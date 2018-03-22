
from django.urls import path

from . import views

app_name = 'config'


urlpatterns = [
    path('settings/', views.ConfigurationUpdateView.as_view(), name='configuration-update'),
]
