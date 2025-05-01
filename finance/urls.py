from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-income/', views.add_income, name='add_income'),
    path('edit-expense/<int:pk>', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('edit-income/<int:pk>', views.edit_income, name = 'edit_income'),
    path('delete-income/<int:pk>/', views.delete_income, name='delete_income'),
    path('login/', LoginView.as_view(template_name='finance/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),
]
