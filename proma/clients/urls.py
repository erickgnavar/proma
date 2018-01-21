from django.urls import path

from . import views

app_name = 'clients'


urlpatterns = [
    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:id>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('clients/<int:id>/update/', views.ClientUpdateView.as_view(), name='client-update'),
]
