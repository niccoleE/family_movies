from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


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
        else:
            for text in form.errors.values():
                print(text)



    context = {'form': form}
    return render(request, 'registration/register.html', context)
