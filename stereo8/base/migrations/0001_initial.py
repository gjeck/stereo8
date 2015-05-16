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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('date', models.DateField()),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('popularity', models.FloatField(default=0.0)),
                ('score', models.IntegerField(default=0)),
                ('score_url', models.URLField()),
                ('summary', models.TextField()),
                ('spotify_id', models.CharField(default='', max_length=255)),
                ('spotify_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('bio', models.TextField()),
                ('bio_url', models.URLField()),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('familiarity', models.FloatField(default=0.0)),
                ('spotify_id', models.CharField(default='', max_length=255)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('large', models.URLField()),
                ('mbid', models.CharField(unique=True, max_length=255)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('score', models.IntegerField()),
                ('summary', models.TextField()),
                ('album', models.ForeignKey(to='base.Album', null=True, blank=True)),
                ('publisher', models.ForeignKey(to='base.Publisher', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('duration', models.IntegerField()),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('spotify_id', models.CharField(default='', max_length=255)),
                ('spotify_url', models.URLField(blank=True, null=True)),
                ('album', models.ForeignKey(to='base.Album', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='artist',
            name='image',
            field=models.ForeignKey(to='base.Image', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='tags',
            field=taggit.managers.TaggableManager(verbose_name='Tags', through='taggit.TaggedItem', to='taggit.Tag', help_text='A comma-separated list of tags.'),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(to='base.Artist', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='album',
            name='image',
            field=models.ForeignKey(to='base.Image', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='album',
            name='tags',
            field=taggit.managers.TaggableManager(verbose_name='Tags', through='taggit.TaggedItem', to='taggit.Tag', help_text='A comma-separated list of tags.'),
        ),
    ]
