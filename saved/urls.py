from django.urls import path
from . import views


urlpatterns = [
    path('create-admin/',views.create_admin,name='create-admin'),
    path('login/',views.custom_login, name='login'),
    path('',views.home, name='home'),
    path('register', views.register, name='register'),
    path('news', views.send_news, name="send_news"),
    path('saved', views.view_saved, name="saved"),
]