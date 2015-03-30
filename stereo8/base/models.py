from django.db import models

class Album(models.Model):
    artist = models.ForeignKey('Artist')
    label = models.ForeignKey('Label')
    images = models.ManyToManyField('Image')
    date = models.DateField()
    title = models.CharField(max_length=255)
    summary = models.TextField()
    score = models.IntegerField()

class Artist(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()

class Image(models.Model):
    small = models.URLField()
    large = models.URLField()

class Label(models.Model):
    name = models.CharField(max_length=255)

class Publisher(models.Model):
    name = models.CharField(max_length=255)

class Review(models.Model):
    album = models.ForeignKey('Album')
    publisher = models.ForeignKey('Publisher')
    summary = models.TextField()
    score = models.IntegerField()
    date = models.DateField()

class Track(models.Model):
    artist = models.ForeignKey('Artist')
    title = models.CharField(max_length=255)
    duration = models.IntegerField()
    url = models.URLField()

