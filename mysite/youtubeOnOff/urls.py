from django.urls import path

from . import views

urlpatterns = [
    path('list', views.index, name='index'),
    path('create_onoff', views.create_onoff, name='create_onoff'),
    path('edit_onoff/<int:onoff_id>/', views.edit_onoff, name='edit_onoff'),
    path('delete_onoff/<int:onoff_id>/', views.delete_onoff, name='delete_onoff')
]