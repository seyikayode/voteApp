from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegisterForm
# Create your views here.
def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            messages.success(request, f'Welcome {username}!')
            login(request, user)
            return redirect('polls:list')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)













