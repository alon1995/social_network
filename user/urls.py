from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_users, name='all-users'),
    path('new_user', views.create_new_user, name="new_user"),
    path('delete_user/<int:pk>/', views.delete_user, name="delete_user"),
    path('update_user/<int:pk>/', views.update_user, name="update_user")
]