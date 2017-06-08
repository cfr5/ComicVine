# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-07 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comics', '0002_auto_20170607_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.CharField(max_length=50, primary_key='true', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('alias', models.CharField(max_length=100)),
                ('birth_date', models.CharField(max_length=100)),
                ('biography', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('character_id', models.CharField(max_length=50, primary_key='true', serialize=False)),
                ('super_name', models.CharField(max_length=100)),
                ('real_name', models.CharField(max_length=100)),
                ('aliases', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('character_type', models.CharField(max_length=100)),
                ('powers', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=100)),
                ('origin', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('comic_id', models.CharField(max_length=50, primary_key='true', serialize=False)),
                ('issue_number', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=100)),
                ('store_date', models.CharField(max_length=100)),
                ('synopsis', models.CharField(max_length=10000)),
                ('characters', models.ManyToManyField(to='comics.Character', verbose_name='list of characters')),
            ],
        ),
        migrations.CreateModel(
            name='UserFollows',
            fields=[
                ('user_id', models.CharField(max_length=50, primary_key='true', serialize=False)),
                ('authors', models.ManyToManyField(to='comics.Author', verbose_name='list of authors')),
                ('characters', models.ManyToManyField(to='comics.Character', verbose_name='list of characters')),
                ('comics', models.ManyToManyField(to='comics.Comic', verbose_name='list of comics')),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='comics',
            field=models.ManyToManyField(to='comics.Comic', verbose_name='list of comics'),
        ),
    ]