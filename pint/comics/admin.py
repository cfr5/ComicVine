# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from comics.models import Character, Comic, Author, UserFollows
# Register your models here.

admin.site.register(Character)
admin.site.register(Comic)
admin.site.register(Author)
admin.site.register(UserFollows)
