from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Movie, Comment
from .forms import MovieForm, CommentForm, SelectForm, ReviewForm, AddForm

import requests

TMDB_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
TMDB_Key = 'cc543d2d9414e851a83e46e2fa1a5a57'
TMDB_IMG = "https://image.tmdb.org/t/p/w500"


def home(request):
    movies = Movie.objects.order_by('-rating')
    context = {'movies': movies}
    return render(request, 'my_movies/index.html', context)


@login_required
def my_movies(request):
    movies = Movie.objects.filter(owner=request.user).order_by('-date_added')
    context = {'movies': movies}
    return render(request, 'my_movies/all_movies.html', context)


@login_required
def user_movies(request, owner):
    movies = Movie.objects.filter(owner__username=owner).order_by('-date_added')
    context = {'movies': movies, 'owner': owner}
    return render(request, 'my_movies/all_movies.html', context)


@login_required
def movie(request, movie_id):
    """Show a single movie and all its comments"""
    movie = Movie.objects.get(id=movie_id)
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

            if tmdb_movies:
                context = {'movies': tmdb_movies}
                return render(request, 'my_movies/select.html', context)
            else:

                return redirect('my_movies:not_tmdb')

    context = {'form': form}
    return render(request, 'my_movies/add.html', context)


@login_required
def select(request):
    """find movie in TMDB movie"""
    if request.method != 'POST':
        form = SelectForm()
    else:
        form = SelectForm(data=request.POST)
        if form.is_valid():
            title = request.POST['title']
            response = requests.get("https://api.themoviedb.org/3/search/movie",
                                    params={"api_key": TMDB_Key, "query": title})
            tmdb_movies = response.json()['results']
            context = {'movies': tmdb_movies}
            return render(request, 'my_movies/select.html', context)
    context = {'form': form}
    return render(request, 'my_movies/add.html', context)


@login_required
def find(request, db_id):
    """get TMDB movie details"""
    response = requests.get(f"https://api.themoviedb.org/3/movie/{db_id}", params={'api_key': TMDB_Key})
    selected_movie = response.json()

    try:
        new_movie = Movie(
            title=selected_movie['title'],
            owner=request.user,
            year=selected_movie['release_date'].split("-")[0],
            description=selected_movie['overview'],
            homepage=selected_movie['homepage'],
            img_url=f"{TMDB_IMG}{selected_movie['poster_path']}",
            genre=selected_movie['genres'][0]['name'],
        )
    except ValueError:
        return redirect('my_movies:select')
    except IndexError:
        return redirect('my_movies:select')
    new_movie.save()

    context = {'movie': new_movie}
    return render(request, 'my_movies/saving.html', context)


@login_required
def not_tmdb(request):
    title = request.session['title']
    if request.method != "POST":
        form = MovieForm()
    else:
        form = MovieForm(data=request.POST)
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
    print(movie.title)
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
def review(request, movie_id):
    """add review and rating"""
    movie = Movie.objects.get(id=movie_id)
    if movie.owner != request.user:
        raise Http404
    if request.method != 'POST':
        review_form = ReviewForm(instance=movie)
    else:
        review_form = ReviewForm(instance=movie, data=request.POST)
        if review_form.is_valid():
            movie.review = request.POST['review']
            movie.rating = request.POST['rating']
            review_form.save()
            return redirect('my_movies:home')
        else:
            print(review_form.errors)

    context = {'movie': movie, 'form': review_form}
    return render(request, 'my_movies/review.html', context)


@login_required
def delete(request, movie_id):
    """delete movie"""
    movie = Movie.objects.get(id=movie_id)
    if movie.owner != request.user:
        raise Http404
    movie.delete()
    return redirect('my_movies:my_movies')


@login_required
def cancel(request, movie_id):
    """delete movie"""
    movie = Movie.objects.get(id=movie_id)
    if movie.owner != request.user:
        raise Http404
    movie.delete()
    return redirect('my_movies:add')


@login_required
def new_comment(request, movie_id):
    """add a new comment for a particular movie"""
    movie = Movie.objects.get(id=movie_id)

    if request.method != 'POST':
        # create an empty form
        form = CommentForm()
    else:
        print(f'method post ')
        parent_id = request.POST.get('parentId')
        if parent_id:
            print(parent_id)
            parent = Comment.objects.get(id=parent_id)
            text = request.POST.get('reply')
            comment_reply = Comment(text=text, owner=request.user, movie=movie, parent=parent)
            comment_reply.save()
        else:
            print("new comment")
            form = CommentForm(data=request.POST)

            if form.is_valid():
                print('form is valid')
                new_comment = form.save(commit=False)
                new_comment.movie = movie
                new_comment.owner = request.user
                new_comment.save()

        return redirect("my_movies:see_comments", movie_id=movie_id)

    # show an empty form
    context = {'movie': movie, 'form': form}
    return render(request, 'my_movies/new_comment.html', context)


@login_required()
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
