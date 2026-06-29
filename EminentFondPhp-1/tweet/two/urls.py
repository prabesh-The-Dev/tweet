from . import views
from django.urls import path

urlpatterns = [
    path('', views.form, name='form'),
    path('index/', views.index, name='index'),
    path('add_tweet/', views.add_tweet, name='add_tweet'),
    path('delete_tweet/<int:tweet_id>/', views.delete_tweet, name='delete_tweet'),
    path('login/', views.login, name='login'),
    path('edit_tweet/<int:tweet_id>/', views.edit_tweet, name='edit_tweet'),
    path('register/', views.register, name='register'),
]
