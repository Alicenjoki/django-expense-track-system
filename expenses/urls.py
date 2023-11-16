from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views


urlpatterns =[
    path('home/', home, name='home'),
    path('expenses/', expenses, name='expenses'),
    path('add_expense/', add_expense, name='add_expense'),
    path('edit_expense/<uuid>/', edit_expense, name='edit_expense'),
    path('search_expenses/',csrf_exempt(search_expenses), name='search_expenses'),
]