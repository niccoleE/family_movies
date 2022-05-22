"""Defines URL patterns for My movies"""

from django.urls import path
from . import views

app_name = 'my_movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('my_movies/', views.my_movies, name='my_movies'),
    path('movies/author<owner>/', views.user_movies, name='user_movies'),
    path('movies/<int:movie_id>/', views.movie, name='movie'),
    path('movies/comments/<int:movie_id>/', views.see_comments, name='see_comments'),
    path('review/<int:movie_id>/', views.review, name='review'),
    path('find/<int:db_id>/', views.find, name='find'),
    path('add_post/', views.add, name='add'),
    path('select/', views.select, name='select'),
    path('movies/<int:movie_id>/delete/', views.delete, name='delete'),
    path('cancel/<int:movie_id>/', views.cancel, name='cancel'),
    path('edit/<int:movie_id>/', views.edit, name='edit'),
    path('new_comment/<int:movie_id>/', views.new_comment, name='new_comment'),
    path('not_tmdb/', views.not_tmdb, name="not_tmdb"),
]
