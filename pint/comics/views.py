# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd
import numpy as np

from comics.forms import UserCreationForm

from comics.models import Comic, Character, Author, CharacterFollows

# Create your views here.
@login_required()
def index(request):
    context = {'comics': Comic.objects.all(),'characters': Character.objects.all(),'authors': Author.objects.all()}
    return render(request, 'comics/index.html', context)

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
def comic(request, comic_id):
    context = {'comic': Comic.objects.get(pk=comic_id)}
    return render(request, 'comics/comic.html',context)

@login_required()
def author(request, author_id):
    context = {'author': Author.objects.get(pk=author_id)}
    return render(request, 'comics/author.html',context)

@login_required()
def character(request, character_id):
    context = {'character': Character.objects.get(pk=character_id)}
    return render(request, 'comics/character.html',context)

def test(request):
    #c= Character(character_id=1,super_name='Mr Chaman',real_name='Ignatius',aliases= 'pollito',publisher='ser',gender='male',character_type='human',powers='all',image='http://4www.ecestaticos.com/imagestatic/clipping/491/e81/491e810bc7d83a6dbe8d51a5948d55b4/la-buena-mierda-fascista-de-ignatius-farray-en-la-cama-con-la-bestia-parda-del-humor.jpg',origin='Canarias')
    #c.save()
    d=CharacterFollows(character=Character.objects.get(pk=1),user_id='oscar')
    d.save()
    print((CharacterFollows.objects.get(user_id='oscar')).follows)

    return redirect('index')




@login_required()
def statistics(request):
	
	fig=plt
	plt.plot([1,2,3,4])
	plt.ylabel('some numbers')
	fig.savefig('comics/static/statistics/table.png')
	return render(request, 'config/statistics.html')












