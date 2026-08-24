from main.models import Category
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('main:product_list')
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('main:product_list')
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('main:product_list')

@login_required
def profile_view(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'accounts/profile.html', context)
