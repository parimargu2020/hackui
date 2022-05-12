from django.urls import path
from . import views

urlpatterns = [
    path('', views.name_pronunciation, name = 'name_pronunciation'),
]