from django.urls import path
from . import views

urlpatterns = [
  path('accounts/<str:login_or_register_param>/', views.user_login_and_register, name='login-register'),
  path('vegetable-recommendations/', views.vegetable_recommendations, name='vegetable_recommendations'),
  path('cultural-management-practices/', views.cultural_management_practices, name='cultural_management_practices'),
  path('nutrient-management/', views.nutrient_management, name='nutrient_management'),
  path('home/', views.home, name='home'),
  path('', views.home, name='home'),

  path('logout/', views.user_logout, name='logout'),
]