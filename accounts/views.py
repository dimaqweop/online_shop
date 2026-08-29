from config import middleware
from main.models import Category
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileEditForm
from django.contrib import messages

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

@login_required
def profile_edit(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Ваш профіль успішно оновлено!")
            return redirect('accounts:profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'categories': categories,
        'title': 'Редагування профілю'
    })
