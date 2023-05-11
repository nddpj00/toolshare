from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_items, name='items'),
    path('<int:item_id>/', views.item_detail, name='item_detail'),
    path('add/', views.add_item, name='add_item'),
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]
