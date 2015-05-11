from django.db import models
from taggit.managers import TaggableManager

class Album(models.Model):
    artist = models.ForeignKey('Artist', blank=True, null=True)
    image = models.ForeignKey('Image', blank=True, null=True)
    label = models.ForeignKey('Label', blank=True, null=True)
    tags = TaggableManager()
    date = models.DateField()
    mbid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    score = models.IntegerField()
    score_url = models.URLField()
    summary = models.TextField()
    def __str__(self):
        album = (self.name, getattr(self.artist, 'name', '(None)'))
        return '{0} - {1}'.format(*album)

class Artist(models.Model):
    tags = TaggableManager()
    bio = models.TextField()
    bio_url = models.URLField()
    mbid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Image(models.Model):
    large = models.URLField()
    mbid = models.CharField(max_length=255, unique=True)
    medium = models.URLField()
    small = models.URLField()

class Label(models.Model):
    mbid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    def __str__(self):
        return self.name

class Review(models.Model):
    album = models.ForeignKey('Album', blank=True, null=True)
    publisher = models.ForeignKey('Publisher', blank=True, null=True)
    date = models.DateField()
    score = models.IntegerField()
    summary = models.TextField()
    def __str__(self):
        review = (
            getattr(self.publisher, 'name', '(None)'),
            getattr(self.album, 'name', '(None)'),
            self.score
        )
        return '{0} - {1} - {2}'.format(*review)

class Track(models.Model):
    album = models.ForeignKey('Album', blank=True, null=True)
    duration = models.IntegerField()
    mbid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        track = (getattr(self.album, 'name', '(None'), self.name)
        return '{0} - {1}'.format(*track)

