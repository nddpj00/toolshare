from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='blog'),
    path('add/', views.add_article, name='add_article'),
    path('edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('delete/<int:instance_id>/', views.delete_instance_blog, name='delete_instance_blog'),
    path('<slug:slug>/', views.article_detail, name ='detail'),
]