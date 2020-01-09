from django.urls import path, include

from . import views

app_name = 'game'

urlpatterns = [
    path( '', views.index, name='index'),

]
