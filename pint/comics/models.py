# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Character (models.Model):
    character_id = models.CharField(max_length=50,primary_key = 'true')
    super_name = models.CharField(max_length=1000)
    real_name = models.CharField(max_length=1000)
    aliases = models.CharField(max_length=1000)
    publisher = models.CharField(max_length=1000)
    gender = models.CharField(max_length=1000)
    character_type = models.CharField(max_length=1000)
    powers = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)
    origin = models.CharField(max_length=10000)
    def __unicode__(self):
        return self.character_id

class Comic (models.Model):
    comic_id = models.CharField(max_length=50,primary_key = 'true')
    issue_number = models.IntegerField()
    title = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)
    characters = models.ManyToManyField(Character, verbose_name="list of characters")
    store_date = models.CharField(max_length=1000)
    synopsis = models.CharField(max_length=10000)
    def __unicode__(self):
        return self.comic_id

class Author (models.Model):
    author_id = models.CharField(max_length=50,primary_key = 'true')
    name = models.CharField(max_length=1000)
    comics = models.ManyToManyField(Comic, verbose_name="list of comics")
    town = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)
    gender = models.CharField(max_length=1000)
    alias = models.CharField(max_length=1000)
    birth_date = models.CharField(max_length=1000)
    biography = models.CharField(max_length=10000)
    image = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.author_id
'''
class UserFollows (models.Model):
    user_id = models.CharField(max_length=50,primary_key = 'true')
    characters = models.ManyToManyField(Character, verbose_name="list of characters")
    comics = models.ManyToManyField(Comic, verbose_name="list of comics")
    authors = models.ManyToManyField(Author, verbose_name="list of authors")
'''

class ComicFollows(models.Model):
    follows_id = models.AutoField(primary_key=True)
    comic = models.OneToOneField(Comic)
    user_id = models.CharField(max_length=50)
    follows = models.DateTimeField(auto_now=True)

class AuthorFollows(models.Model):
    follows_id = models.AutoField(primary_key=True)
    author = models.OneToOneField(Author)
    user_id = models.CharField(max_length=50)
    follows = models.DateTimeField(auto_now=True)

class CharacterFollows(models.Model):
    follows_id = models.AutoField(primary_key=True)
    character = models.OneToOneField(Character)
    user_id = models.CharField(max_length=50)
    follows = models.DateTimeField(auto_now=True)
