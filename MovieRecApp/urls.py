from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('', views.recommend_movies, name='recommend_movies'),

]
