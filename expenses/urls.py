from django.urls import path
from . import views

urlpatterns = [
    # Auth URLs
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main pages
    path('', views.home, name='home'),
    path('add/', views.add_expense, name='add_expense'),
    path('expense/<int:pk>/edit/', views.edit_expense, name='edit_expense'),
    path('expense/<int:pk>/delete/', views.delete_expense, name='delete_expense'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('analytics/', views.analytics, name='analytics'),
    path('profile/', views.profile, name='profile'),
]
