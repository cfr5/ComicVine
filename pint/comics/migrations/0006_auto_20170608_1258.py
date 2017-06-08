# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-08 10:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0005_auto_20170608_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='comics',
        ),
        migrations.AlterUniqueTogether(
            name='authorfollows',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='authorfollows',
            name='author',
        ),
        migrations.AlterUniqueTogether(
            name='characterfollows',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='characterfollows',
            name='character',
        ),
        migrations.RemoveField(
            model_name='comic',
            name='characters',
        ),
        migrations.AlterUniqueTogether(
            name='comicfollows',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='comicfollows',
            name='comic',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='AuthorFollows',
        ),
        migrations.DeleteModel(
            name='Character',
        ),
        migrations.DeleteModel(
            name='CharacterFollows',
        ),
        migrations.DeleteModel(
            name='Comic',
        ),
        migrations.DeleteModel(
            name='ComicFollows',
        ),
    ]