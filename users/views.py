from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User


def register(request):
    """Register a new user"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('my_movies:home')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


def login_check(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        check_username = request.POST['username']
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("my_movies:home")
        else:
            if User.objects.filter(username=check_username).exists():
                print("exists")
                messages.error(request, "Invalid password.")
            else:
                messages.error(request, "No such user. Please check the username"
                                        " or register if you haven't registered yet")
                return redirect("users:login_check")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "registration/login.html", context)
