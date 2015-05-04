# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('score', models.IntegerField()),
                ('score_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('bio', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('small', models.URLField()),
                ('large', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('summary', models.TextField()),
                ('score', models.IntegerField()),
                ('date', models.DateField()),
                ('album', models.ForeignKey(to='base.Album', null=True, blank=True)),
                ('publisher', models.ForeignKey(to='base.Publisher', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('mbid', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('duration', models.IntegerField()),
                ('album', models.ForeignKey(to='base.Album', null=True, blank=True)),
                ('artist', models.ForeignKey(to='base.Artist', null=True, blank=True)),
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
    ]
