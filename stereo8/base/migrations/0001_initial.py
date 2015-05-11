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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('score', models.IntegerField()),
                ('score_url', models.URLField()),
                ('summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('bio_url', models.URLField()),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', to='taggit.Tag', verbose_name='Tags', through='taggit.TaggedItem')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('large', models.URLField()),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('medium', models.URLField()),
                ('small', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=255)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('score', models.IntegerField()),
                ('summary', models.TextField()),
                ('album', models.ForeignKey(to='base.Album', null=True, blank=True)),
                ('publisher', models.ForeignKey(to='base.Publisher', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField()),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('album', models.ForeignKey(to='base.Album', null=True, blank=True)),
            ],
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
            name='label',
            field=models.ForeignKey(to='base.Label', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='album',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', to='taggit.Tag', verbose_name='Tags', through='taggit.TaggedItem'),
        ),
    ]
