"""Defines URL patterns for My movies"""

from django.urls import path
from . import views

app_name = 'my_movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('all/', views.all, name='all'),
    path('last10/', views.last_added, name='last_added'),
    path('top10/', views.top10, name='top10'),
    path('by_user/', views.by_user, name='by_user'),
    path('my_movies/', views.my_movies, name='my_movies'),
    path('movies/author<owner>/', views.user_movies, name='user_movies'),
    path('movies/<int:movie_id>/', views.movie, name='movie'),
    path('movies/comments/<int:movie_id>/', views.see_comments, name='see_comments'),
    path('find/<int:db_id>/', views.find, name='find'),
    path('add_post/', views.add, name='add'),
    path('movies/<int:movie_id>/delete/', views.delete, name='delete'),
    path('edit/<int:movie_id>/', views.edit, name='edit'),
    path('new_comment/<int:movie_id>/', views.new_comment, name='new_comment'),
    path('not_tmdb/', views.not_tmdb, name="not_tmdb"),
    path('wish_list/', views.wish_list, name="wish_list"),
    path('watch_list/<int:movie_id>', views.add_to_watchlist, name="add_to_watchlist"),
    path('favorite/', views.favorite, name="favorite"),
    path('favorite/<int:movie_id>', views.delete_from_watchlist, name="delete_from_watchlist"),
    path('note/<int:note_id>', views.delete_note, name="delete_note"),
]
