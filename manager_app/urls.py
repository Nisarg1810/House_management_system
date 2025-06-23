from django.urls import path
from . import views

app_name = 'manager_app'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('budget/', views.budget_view, name='budget'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('profile/', views.profile_view, name='profile'),
]