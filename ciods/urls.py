from django.urls import path
from . import views

app_name = 'ciods'

urlpatterns = [
path('',views.ciods, name = 'ciods'),
]
