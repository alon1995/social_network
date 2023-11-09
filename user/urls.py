from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_users, name='all-users'),
    path('signup', views.signup, name="signup"),
    path('delete_user/<int:pk>/', views.delete_user, name="delete_user"),
    path('update_user/<int:pk>/', views.update_user, name="update_user"),
    path('login/', views.CustomUserLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]