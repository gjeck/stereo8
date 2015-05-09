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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('bio', models.TextField()),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('large', models.URLField()),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('small', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField()),
                ('score', models.IntegerField()),
                ('summary', models.TextField()),
                ('album', models.ForeignKey(blank=True, null=True, to='base.Album')),
                ('publisher', models.ForeignKey(blank=True, null=True, to='base.Publisher')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('duration', models.IntegerField()),
                ('mbid', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('album', models.ForeignKey(blank=True, null=True, to='base.Album')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(blank=True, null=True, to='base.Artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='image',
            field=models.ForeignKey(blank=True, null=True, to='base.Image'),
        ),
        migrations.AddField(
            model_name='album',
            name='label',
            field=models.ForeignKey(blank=True, null=True, to='base.Label'),
        ),
        migrations.AddField(
            model_name='album',
            name='tags',
            field=taggit.managers.TaggableManager(through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags', help_text='A comma-separated list of tags.'),
        ),
    ]
