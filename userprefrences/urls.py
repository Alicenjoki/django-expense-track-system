from django.urls import  path
from .views import *

urlpatterns=[
    path('prefered/', prefered, name='prefered'),
]