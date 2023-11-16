from django.urls import path
from .views import *

urlpatterns =[
    path('income/', income, name='income'),
    path('add_income/', add_income, name='add_income'),
    path('edit_income/<uuid>/', edit_income, name='edit_income'),
    path('delete_income/<uuid>/', delete_income, name='delete_income'),
]