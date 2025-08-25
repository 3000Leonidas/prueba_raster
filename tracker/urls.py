from django.urls import path
from . import views

urlpatterns = [
    #para crear un nuevo rastreador
    path('create/', views.create_tracker, name='create_tracker'),

    #para el rastreador de imagen que usara un id unico
    path('<uuid:tracker_id>/', views.track_image, name='track_image'),
]