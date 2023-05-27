from django.urls import path
from newsletter import views


urlpatterns = [
    path('newsletter_form', views.newsletter_form, name='newsletter_form'),
]