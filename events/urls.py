from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_list, name='events'),
    path('add/', views.add_event, name ='add_event'),
    path('<slug:slug>/', views.event_detail, name ='event_detail'),
]