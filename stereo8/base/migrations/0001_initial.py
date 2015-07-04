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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('spotify_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('bio', models.TextField()),
                ('bio_url', models.URLField()),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('familiarity', models.FloatField(default=0.0)),
                ('spotify_id', models.CharField(max_length=255)),
                ('spotify_url', models.URLField(blank=True, null=True)),
                ('trending', models.FloatField(default=0.0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('large', models.URLField(blank=True, null=True)),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('medium', models.URLField(blank=True, null=True)),
                ('small', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
            name='SonicInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('acousticness', models.FloatField(default=0.0)),
                ('danceability', models.FloatField(default=0.0)),
                ('energy', models.FloatField(default=0.0)),
                ('instrumentalness', models.FloatField(default=0.0)),
                ('liveness', models.FloatField(default=0.0)),
                ('loudness', models.FloatField(default=0.0)),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('speechiness', models.FloatField(default=0.0)),
                ('tempo', models.FloatField(default=0.0)),
                ('valence', models.FloatField(default=0.0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('duration', models.IntegerField()),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('spotify_id', models.CharField(max_length=255)),
                ('spotify_url', models.URLField(blank=True, null=True)),
                ('album', models.ForeignKey(blank=True, to='base.Album', null=True)),
                ('sonic_info', models.ForeignKey(blank=True, to='base.SonicInfo', null=True)),
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
            name='sonic_info',
            field=models.ForeignKey(blank=True, to='base.SonicInfo', null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', verbose_name='Tags', help_text='A comma-separated list of tags.'),
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
            name='sonic_info',
            field=models.ForeignKey(blank=True, to='base.SonicInfo', null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', verbose_name='Tags', help_text='A comma-separated list of tags.'),
        ),
    ]
