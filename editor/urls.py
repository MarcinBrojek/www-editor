from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get/ajax/files_list', views.files_list, name='files_list'),
    path('get/ajax/add', views.add, name='add'),
    path('get/ajax/remove', views.remove, name='remove'),
    path('get/ajax/log_in', views.log_in, name='log_in'),
    path('get/ajax/register', views.register, name='register'),
    path('get/ajax/rerun', views.rerun, name='rerun'),
    path('get/ajax/rerun/result', views.result, name='result')
]
