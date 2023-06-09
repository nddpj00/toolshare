from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_list, name='events_list'),
    path('add/', views.add_event, name ='add_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:instance_id>/', views.delete_instance_event, name='delete_instance_event'),
    path('<slug:slug>/', views.event_detail, name ='event_detail'),
    path('add_attendee/<int:event_id>', views.add_attendee, name='add_attendee'),
    path('add_interested/<int:event_id>', views.add_interested, name='add_interested'),
]