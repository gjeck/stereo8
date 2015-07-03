# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('date', models.DateField()),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('popularity', models.FloatField(default=0.0)),
                ('score', models.IntegerField(default=0)),
                ('score_url', models.URLField()),
                ('summary', models.TextField()),
                ('spotify_id', models.CharField(max_length=255)),
                ('spotify_url', models.URLField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('bio', models.TextField()),
                ('bio_url', models.URLField()),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('familiarity', models.FloatField(default=0.0)),
                ('spotify_id', models.CharField(max_length=255)),
                ('spotify_url', models.URLField(null=True, blank=True)),
                ('trending', models.FloatField(default=0.0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('large', models.URLField(null=True, blank=True)),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('medium', models.URLField(null=True, blank=True)),
                ('small', models.URLField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('score', models.IntegerField()),
                ('summary', models.TextField()),
                ('url', models.URLField(unique=True)),
                ('album', models.ForeignKey(blank=True, to='base.Album', null=True)),
                ('publisher', models.ForeignKey(blank=True, to='base.Publisher', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('acousticness', models.FloatField(default=0.0)),
                ('danceability', models.FloatField(default=0.0)),
                ('duration', models.IntegerField()),
                ('energy', models.FloatField(default=0.0)),
                ('instrumentalness', models.FloatField(default=0.0)),
                ('liveness', models.FloatField(default=0.0)),
                ('loudness', models.FloatField(default=0.0)),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('speechiness', models.FloatField(default=0.0)),
                ('spotify_id', models.CharField(max_length=255)),
                ('spotify_url', models.URLField(null=True, blank=True)),
                ('tempo', models.FloatField(default=0.0)),
                ('valence', models.FloatField(default=0.0)),
                ('album', models.ForeignKey(blank=True, to='base.Album', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='artist',
            name='image',
            field=models.ForeignKey(blank=True, to='base.Image', null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='tags',
            field=taggit.managers.TaggableManager(verbose_name='Tags', to='taggit.Tag', help_text='A comma-separated list of tags.', through='taggit.TaggedItem'),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(blank=True, to='base.Artist', null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='image',
            field=models.ForeignKey(blank=True, to='base.Image', null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='tags',
            field=taggit.managers.TaggableManager(verbose_name='Tags', to='taggit.Tag', help_text='A comma-separated list of tags.', through='taggit.TaggedItem'),
        ),
    ]
