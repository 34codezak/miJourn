# entries/urls.py
from django.urls import path
from . import views

app_name = 'entries'

urlpatterns = [
    path('', views.home, name='home'),
    path('all/', views.view_all_entries, name='view_all_entries'),
    path('create/', views.create_entry, name='create_entry'),
    path('<int:entry_id>/', views.view_entry, name='view_entry'),
    path('<int:entry_id>/update/', views.update_entry, name='update_entry'),
    path('<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
    path('search/', views.search_entries, name='search_entries'),
    path('delete/multiple/', views.multi_delete, name='multi_delete'),
]