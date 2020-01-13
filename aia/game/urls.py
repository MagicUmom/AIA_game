from django.urls import path, include

from . import views

app_name = 'game'

urlpatterns = [
    path( '', views.index, name='index'),
    path( 'controll_pannel/', views.controll_pannel, name='controll_pannel'),

    path( 'admin_api/game_over', views.admin_api_game_over, name='admin_api_game_over' ),
    path( 'admin_api/new_game',  views.admin_api_new_game,  name='admin_api_new_game' ),
    path( 'admin_api/confirm',   views.admin_api_confirm,   name='admin_api_confirm' ),
    path( 'admin_api/lock',      views.admin_api_lock,      name='admin_api_lock' ),
]
