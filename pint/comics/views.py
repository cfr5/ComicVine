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
    follows = ComicFollows.objects.filter(comic=comic_id,user_id=request.user).count()

    if Comic.objects.filter(pk=comic_id).count():
        return render(request, 'comics/comic.html',{'comic': Comic.objects.get(pk=comic_id), 'follows': follows})
    else:
        headers = {'User-Agent': 'PintGrupo10'}
        response = requests.get('https://comicvine.gamespot.com/api/issue/4000-'+comic_id, params={'format': 'json', 'api_key': settings.COMICVINE_KEY}, headers=headers)
        if response.status_code == 200:
            son = json.loads(response.text)
            results = son['results']
            if results:
                comic_id=results['id']
                issue_number=results['issue_number']
                if not issue_number:
                    issue_number= 0
                title=results['name']
                if not title:
                    title= "Title not available"
                image=results['image']['super_url']
                store_date=results['cover_date']
                if not store_date:
                    store_date= "0000-00-00"
                synopsis=results['description']
                if not synopsis:
                    synopsis = "Synopsis not available"
                Comic(comic_id,issue_number,title,image,store_date,synopsis).save()

                return render(request, 'comics/comic.html', {'comic': Comic.objects.get(pk=comic_id), 'follows': follows})

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

    plt.clf()

    #Type
    type_characters= df_characters.groupby('character_type').count()['character_id']
    p_characters_type= type_characters.plot(legend=False,kind='barh',figsize=(8,3))
    p_characters_type.get_figure().savefig('comics/static/statistics/characters_type.png')

    plt.clf()

    #Publisher
    publisher_characters= df_characters.groupby('publisher').count()['character_id']
    p_characters_publisher= publisher_characters.plot(legend=False,kind='barh',figsize=(8,3))
    p_characters_publisher.get_figure().savefig('comics/static/statistics/characters_publisher.png')

    plt.clf()

    #Powers
    powers_characters= df_characters.groupby('powers').count()['character_id']
    p_characters_powers= powers_characters.plot(legend=False,kind='barh',figsize=(8,3))
    p_characters_powers.get_figure().savefig('comics/static/statistics/characters_powers.png')

    plt.clf()

    #Authors
    authors= Author.objects.all()
    query_authors = str(authors.query)
    df_authors = pd.read_sql_query(query_authors, connection)


    #Genero
    gender_authors=df_authors.groupby('gender').count()['author_id']
    p_authors_gender= gender_authors.plot(legend=False,kind='barh',figsize=(8,3))
    p_authors_gender.get_figure().savefig('comics/static/statistics/authors_gender.png')

    plt.clf()

    #Country
    country_authors=df_authors.groupby('country').count()['author_id']
    p_authors_country= country_authors.plot(legend=False,kind='barh',figsize=(8,3))
    p_authors_country.get_figure().savefig('comics/static/statistics/authors_country.png')

    plt.clf()

    dictionary_authors={}
    year_author=1900
    for year_author in range(1900,2018):
        st_year_author=str(year_author)
        age_authors=df_authors['birth_date'].str.contains(st_year_author)
        print(age_authors)
        #age=2017-year
        contador_author=np.sum(age_authors)
        if contador_author>=1:
            dictionary_authors[year_author]=contador_author
            #print(age_authors)
            #print(np.sum(age_authors))
        year_author+=1

    #print(dictionary)
    df_authors_age=DataFrame.from_dict(dictionary_authors,orient='index')
    df_authors_age_sorted=df_authors_age.sort_index(ascending=False)
    #print(df_authors_age)
    p_authors_age= df_authors_age_sorted.plot(legend=False,kind='barh',figsize=(8,3))
    p_authors_age.get_figure().savefig('comics/static/statistics/authors_age.png')

    plt.clf()

    #Comics

    comics= Comic.objects.all()
    query_comics = str(comics.query)
    df_comics = pd.read_sql_query(query_comics, connection)
    print(df_comics)
    dictionary_comics = {}
    month_comic = 1

    for month_comic in range(1,13):
        if month_comic < 10:
            st_month_comic = "-0"+str(month_comic)+"-"
        else:
            st_month_comic = "-"+str(month_comic)+"-"
        print(month_comic)
        comic_permonth = df_comics['store_date'].str.contains(st_month_comic)
        print(comic_permonth)
        #age=2017-year
        contador_comic = np.sum(comic_permonth)
        options_months = {
        1 : "January",
        2 : "February",
        3 : "March",
        4 : "April",
        5 : "May",
        6 : "June",
        7 : "July",
        8 : "August",
        9 : "September",
        10 : "October",
        11 : "Nobember",
        12 : "December"}


        if contador_comic>=1:
            dictionary_comics[options_months[month_comic]]=contador_comic
        #dictionary_comics[month_comic]=contador_comic

        #print(age_authors)
        #print(np.sum(age_authors))
        contador_comic+=1

    #print(dictionary_comics)
    df_comics_month=DataFrame.from_dict(dictionary_comics,orient='index')
    #print(df_comics_month)

    df_comics_month_sorted=df_comics_month.sort_index(ascending=False)

    p_comics_month= df_comics_month_sorted.plot(legend=False,kind='barh',figsize=(8,3))
    p_comics_month.get_figure().savefig('comics/static/statistics/comics_month.png')

    plt.clf()

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
        else:
            ComicFollows.objects.filter(comic=comic_id,user_id=request.user).delete()
        return redirect('comic', comic_id)
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
