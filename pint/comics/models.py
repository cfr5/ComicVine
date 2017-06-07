# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Character (models.Model):
    character_id = models.CharField(max_length=50,primary_key = 'true')
    super_name = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100)
    aliases = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    character_type = models.CharField(max_length=100)
    powers = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    origin = models.CharField(max_length=10000)
    def __unicode__(self):
        return self.character_id

class Comic (models.Model):
    comic_id = models.CharField(max_length=50,primary_key = 'true')
    issue_number = models.IntegerField()
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    characters = models.ManyToManyField(Character, verbose_name="list of characters")
    store_date = models.CharField(max_length=100)
    synopsis = models.CharField(max_length=10000)
    def __unicode__(self):
        return self.comic_id

class Author (models.Model):
    author_id = models.CharField(max_length=50,primary_key = 'true')
    name = models.CharField(max_length=100)
    comics = models.ManyToManyField(Comic, verbose_name="list of comics")
    town = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    birth_date = models.CharField(max_length=100)
    biography = models.CharField(max_length=10000)
    def __unicode__(self):
        return self.author_id

class UserFollows (models.Model):
    user_id = models.CharField(max_length=50,primary_key = 'true')
    characters = models.ManyToManyField(Character, verbose_name="list of characters")
    comics = models.ManyToManyField(Comic, verbose_name="list of comics")
    authors = models.ManyToManyField(Author, verbose_name="list of authors")
