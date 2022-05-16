from django.urls import path
from . import views

urlpatterns = [
    path('', views.name_pronunciation_vw, name = 'name_pronunciation'),
    path('get_voicenames/', views.get_voicenames_vw, name="get_voicenames"),
]