# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from comics.models import Character, Comic, Author, ComicFollows, AuthorFollows, CharacterFollows
# Register your models here.

admin.site.register(Character)
admin.site.register(Comic)
admin.site.register(Author)
admin.site.register(ComicFollows)
admin.site.register(AuthorFollows)
admin.site.register(CharacterFollows)
