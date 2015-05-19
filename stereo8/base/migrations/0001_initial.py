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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('spotify_id', models.CharField(max_length=255, default='')),
                ('spotify_url', models.URLField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('bio', models.TextField()),
                ('bio_url', models.URLField()),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('familiarity', models.FloatField(default=0.0)),
                ('spotify_id', models.CharField(max_length=255, default='')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('large', models.URLField()),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('medium', models.URLField()),
                ('small', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('score', models.IntegerField()),
                ('summary', models.TextField()),
                ('url', models.URLField(unique=True)),
                ('album', models.ForeignKey(null=True, to='base.Album', blank=True)),
                ('publisher', models.ForeignKey(null=True, to='base.Publisher', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('duration', models.IntegerField()),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('spotify_id', models.CharField(max_length=255, default='')),
                ('spotify_url', models.URLField(null=True, blank=True)),
                ('album', models.ForeignKey(null=True, to='base.Album', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='artist',
            name='image',
            field=models.ForeignKey(null=True, to='base.Image', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', verbose_name='Tags', help_text='A comma-separated list of tags.', through='taggit.TaggedItem'),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(null=True, to='base.Artist', blank=True),
        ),
        migrations.AddField(
            model_name='album',
            name='image',
            field=models.ForeignKey(null=True, to='base.Image', blank=True),
        ),
        migrations.AddField(
            model_name='album',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', verbose_name='Tags', help_text='A comma-separated list of tags.', through='taggit.TaggedItem'),
        ),
    ]
