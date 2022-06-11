from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Movie, Comment, Note
from django.contrib.auth.models import User
from .forms import MovieForm, CommentForm, ReviewForm, AddForm, NoteForm

import requests

TMDB_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
TMDB_Key = 'cc543d2d9414e851a83e46e2fa1a5a57'
TMDB_IMG = "https://image.tmdb.org/t/p/w500"


def home(request):
    movies = Movie.objects.order_by('-date_added')[:1]
    context = {'movies': movies}
    return render(request, 'my_movies/home.html', context)


def all(request):
    movies = Movie.objects.order_by('-rating')
    context = {'movies': movies}
    return render(request, 'my_movies/index.html', context)


def last_added(request):
    movies = Movie.objects.order_by('-date_added')[:10]
    context = {'movies': movies}
    return render(request, 'my_movies/index.html', context)


def top10(request):
    movies = Movie.objects.order_by('-rating')[:10]
    context = {'movies': movies}
    return render(request, 'my_movies/index.html', context)


def by_user(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'my_movies/by_user.html', context)


@login_required
def my_movies(request):
    movies = Movie.objects.filter(owner=request.user).order_by('-date_added')
    context = {'movies': movies, 'owner': request.user}
    return render(request, 'my_movies/all_movies.html', context)


def user_movies(request, owner):
    movies = Movie.objects.filter(owner__username=owner).order_by('-date_added')
    context = {'movies': movies, 'owner': owner}
    return render(request, 'my_movies/all_movies.html', context)


def movie(request, movie_id):
    """Show a single movie and all its comments"""
    movie = get_object_or_404(Movie, id=movie_id)
    comments = Comment.objects.filter(movie=movie, parent=None).order_by('-date_added')
    replies = Comment.objects.filter(movie=movie).exclude(parent=None).order_by('-date_added')

    context = {'movie': movie, 'comments': comments, 'replies': replies}

    return render(request, 'my_movies/movie.html', context)


@login_required()
def add(request):
    """add new post"""
    if request.method != 'POST':
        form = AddForm()
    else:
        form = AddForm(data=request.POST)
        if form.is_valid():
            title = request.POST['title']
            request.session['title'] = title

            response = requests.get("https://api.themoviedb.org/3/search/movie",
                                    params={"api_key": TMDB_Key, "query": title})
            tmdb_movies = response.json()['results']
            context = {'movies': tmdb_movies, 'title': title}
            return render(request, 'my_movies/select.html', context)

    context = {'form': form}
    return render(request, 'my_movies/add.html', context)


@login_required
def find(request, db_id):
    """get TMDB movie details"""
    response = requests.get(f"https://api.themoviedb.org/3/movie/{db_id}", params={'api_key': TMDB_Key})
    selected_movie = response.json()

    try:
        genre_db = selected_movie['genres'][0]['name']
    except IndexError:
        genre_db = None

    year_year = selected_movie['release_date'].split("-")[0]

    new_movie = Movie(
        title=selected_movie['title'],
        owner=request.user,
        year=year_year,
        description=selected_movie['overview'],
        homepage=selected_movie['homepage'],
        img_url=f"{TMDB_IMG}{selected_movie['poster_path']}",
        genre=genre_db,
    )

    movie = new_movie
    if movie.owner != request.user:
        raise Http404
    if request.method != 'POST':
        review_form = ReviewForm(instance=movie)
    else:
        review_form = ReviewForm(instance=movie, data=request.POST)
        if review_form.is_valid():
            movie.review = request.POST['review']
            movie.rating = request.POST['rating']
            try:
                movie.save()
            except ValueError:
                movie.year = None
                movie.save()

            return redirect('my_movies:my_movies')

    context = {'movie': movie, 'form': review_form}
    return render(request, 'my_movies/review.html', context)


@login_required
def not_tmdb(request):
    title = request.session['title']
    if request.method != "POST":
        form = ReviewForm()
    else:
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            new_movie = form.save(commit=False)
            new_movie.owner = request.user
            new_movie.title = title
            new_movie.save()
            return redirect('my_movies:home')
    context = {'form': form, 'title': title}
    return render(request, 'my_movies/not_tmdb.html', context)


@login_required
def edit(request, movie_id):
    """edit movie's info"""
    movie = Movie.objects.get(id=movie_id)
    if movie.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = MovieForm(instance=movie)
    else:
        form = MovieForm(instance=movie, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_movies:movie', movie_id=movie.id)
        else:
            print(form.errors)

    context = {'movie': movie, 'form': form}
    return render(request, 'my_movies/edit.html', context)


@login_required
def delete(request, movie_id):
    """delete movie"""
    movie = Movie.objects.get(id=movie_id)
    if movie.owner != request.user:
        raise Http404
    movie.delete()
    return redirect('my_movies:my_movies')


@login_required
def new_comment(request, movie_id):
    """add a new comment for a particular movie"""
    movie = Movie.objects.get(id=movie_id)

    if request.method != 'POST':
        # create an empty form
        form = CommentForm()
    else:
        parent_id = request.POST.get('parentId')
        if parent_id:
            parent = Comment.objects.get(id=parent_id)
            text = request.POST.get('reply')
            comment_reply = Comment(text=text, owner=request.user, movie=movie, parent=parent)
            comment_reply.save()
        else:
            form = CommentForm(data=request.POST)

            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.movie = movie
                new_comment.owner = request.user
                new_comment.save()

        return redirect("my_movies:see_comments", movie_id=movie_id)

    # show an empty form
    context = {'movie': movie, 'form': form}
    return render(request, 'my_movies/new_comment.html', context)


@login_required
def see_comments(request, movie_id):
    """Show all comments to a particular movie"""
    movie = Movie.objects.get(id=movie_id)

    comments = Comment.objects.filter(movie=movie, parent=None).order_by('-date_added')
    replies = Comment.objects.filter(movie=movie).exclude(parent=None).order_by('-date_added')
    replyDict = {}
    for reply in replies:
        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id] = [reply]
        else:
            replyDict[reply.parent.id].append(reply)

    context = {'movie': movie, 'comments': comments, 'replies': replies, 'replyDict': replyDict}
    return render(request, 'my_movies/test.html', context)


@login_required
def wish_list(request):
    favourite_movies = Movie.objects.filter(fan=request.user).order_by('-date_added')
    my_notes = Note.objects.filter(owner=request.user).order_by('-rating')
    context = {'movies': favourite_movies, 'notes': my_notes}
    return render(request, 'my_movies/wish_list.html', context)


@login_required
def add_to_watchlist(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.fan.add(request.user)
    return redirect("my_movies:wish_list")


@login_required
def delete_from_watchlist(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.fan.remove(request.user)
    return redirect("my_movies:wish_list")


@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id)
    note.delete()
    return redirect("my_movies:wish_list")


@login_required
def favorite(request):
    """add new favourite movie"""
    if request.method != 'POST':
        form = NoteForm()
    else:
        form = NoteForm(data=request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.title = request.POST['title']
            note.rating = request.POST['rating']
            note.owner = request.user
            note.save()
            return redirect("my_movies:wish_list")
    context = {'form': form}
    return render(request, "my_movies/favorite.html", context)
