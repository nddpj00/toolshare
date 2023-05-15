from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='blog'),
    path('blog/<slug:slug>/', views.article_detail, name ='detail'),
    path('add/', views.add_article, name='add_article'),
]