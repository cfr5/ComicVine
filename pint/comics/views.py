# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from comics.forms import UserCreationForm
# Create your views here.
@login_required()
def index(request):
    return render(request, 'comics/index.html')



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
	    raw_password2 = form.cleaned_data.get('password2')
	    if (raw_password==raw_password2):
            	user = authenticate(username=username, email=email, password=raw_password)
            	login(request, user)
            	return redirect('index')
	    else: message.error(request, 'Contraseñas deferentes')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required()
def account(request):
    return render(request, 'config/account.html')

@login_required()
def shops(request):
    return render(request, 'config/shops.html')



@login_required()
def statistics(request):
    return render(request, 'config/statistics.html')
