# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd
import numpy as np
from django.db import connection
from comics.forms import UserCreationForm
from comics.models import Comic, Character, Author, CharacterFollows, ComicFollows, AuthorFollows
from django.conf import settings
import requests
import json

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
    if Comic.objects.filter(pk=comic_id).count():
        context = {'comic': Comic.objects.get(pk=comic_id)}
        return render(request, 'comics/comic.html',context)
    else:
        return render(request, 'comics/404.html')

@login_required()
def author(request, author_id):
    if Author.objects.filter(pk=author_id).count():
        context = {'author': Author.objects.get(pk=author_id)}
        return render(request, 'comics/author.html',context)
    else:
        return render(request, 'comics/404.html')

@login_required()
def character(request, character_id):
    if Character.objects.filter(pk=character_id).count():
        context = {'character': Character.objects.get(pk=character_id)}
        return render(request, 'comics/character.html',context)
    else:
        return render(request, 'comics/404.html')

def test(request):
    #c= Character(character_id=1,super_name='Mr Chaman',real_name='Ignatius',aliases= 'pollito',publisher='ser',gender='male',character_type='human',powers='all',image='http://4www.ecestaticos.com/imagestatic/clipping/491/e81/491e810bc7d83a6dbe8d51a5948d55b4/la-buena-mierda-fascista-de-ignatius-farray-en-la-cama-con-la-bestia-parda-del-humor.jpg',origin='Canarias')
    #c.save()
    d=CharacterFollows(character=Character.objects.get(pk=1),user_id='oscar')
    d.save()
    print((CharacterFollows.objects.get(user_id='oscar')).follows)

    return redirect('index')




@login_required()
def statistics(request):
	
	#Characters
	characters= Character.objects.all()
	query_characters = str(characters.query)
	df_characters = pd.read_sql_query(query_characters, connection)
	#Genero
	gender_characters=df_characters.groupby('gender').count()['character_id']
	
	p_characters_gender= gender_characters.plot(legend=False,kind='barh',figsize=(8,3))

	p_characters_gender.get_figure().savefig('comics/static/statistics/characters_gender.png')
	
	#Type
	type_characters= df_characters.groupby('character_type').count()['character_id']
	p_characters_type= type_characters.plot(legend=False,kind='barh',figsize=(8,3))
	p_characters_type.get_figure().savefig('comics/static/statistics/characters_type.png')

	#Publisher
	publisher_characters= df_characters.groupby('publisher').count()['character_id']
	p_characters_publisher= publisher_characters.plot(legend=False,kind='barh',figsize=(8,3))
	p_characters_publisher.get_figure().savefig('comics/static/statistics/characters_publisher.png')
	
	#Powers
	powers_characters= df_characters.groupby('powers').count()['character_id']
	p_characters_powers= powers_characters.plot(legend=False,kind='barh',figsize=(8,3))
	p_characters_powers.get_figure().savefig('comics/static/statistics/characters_powers.png')


	#Authors
	authors= Author.objects.all()
	query_authors = str(authors.query)
	df_authors = pd.read_sql_query(query_authors, connection)

	#Genero
	gender_authors=df_authors.groupby('gender').count()['author_id']
	p_authors_gender= gender_authors.plot(legend=False,kind='barh',figsize=(8,3))
	p_authors_gender.get_figure().savefig('comics/static/statistics/authors_gender.png')
	
	
	#Genero
	country_authors=df_authors.groupby('country').count()['author_id']
	p_authors_country= country_authors.plot(legend=False,kind='barh',figsize=(8,3))
	p_authors_country.get_figure().savefig('comics/static/statistics/authors_country.png')



	return render(request, 'config/statistics.html')

@login_required()
def search(request):
    query = request.GET['query']
    query_type = request.GET['search_param']
    headers = {'User-Agent': 'PintGrupo10'}
    api_key = settings.COMICVINE_KEY
    end_point = 'https://comicvine.gamespot.com/search/'
    limit= 5
    page = request.GET.get('page', 1)
    response = requests.get('https://comicvine.gamespot.com/api/search/', params={'format': 'json', 'api_key': api_key, 'resources': query_type, 'query': query, 'limit' : limit,'limit': limit}, headers=headers)
    son = json.loads(response.text)
    results = son['results']
    results_lenght = len(results)
    return render(request, 'comics/search.html',{'results': results, 'results_lenght': results_lenght, 'query': query, 'query_type': query_type})

@login_required()
def followcomic(request, comic_id):
    if Comic.objects.filter(pk=comic_id).count():
        comic = Comic.objects.get(pk=comic_id)
        if not ComicFollows.objects.filter(comic=comic_id,user_id=request.user):
            ComicFollows(comic=comic,user_id=request.user).save()
        return render(request, 'comics/comic.html')
    else:
        return render(request, 'comics/404.html')

@login_required()
def followauthor(request, author_id):
    if Author.objects.filter(pk=author_id).count():
        author = Author.objects.get(pk=author_id)
        if not AuthorFollows.objects.filter(author=author_id,user_id=request.user):
            AuthorFollows(author=author,user_id=request.user).save()
        return render(request, 'comics/author.html')
    else:
        return render(request, 'comics/404.html')

@login_required()
def followcharacter(request, character_id):
    if Comic.objects.filter(pk=character_id).count():
        character = Character.objects.get(pk=character_id)
        if not CharacterFollows.objects.filter(character=character_id,user_id=request.user):
            CharacterFollows(character=character,user_id=request.user).save()
        return render(request, 'comics/character.html')
    else:
        return render(request, 'comics/404.html')
