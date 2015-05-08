from django.db import models

class Album(models.Model):
    artist = models.ForeignKey('Artist', blank=True, null=True)
    label = models.ForeignKey('Label', blank=True, null=True)
    image = models.ForeignKey('Image', blank=True, null=True)
    mbid = models.CharField(max_length=255, unique=True)
    date = models.DateField()
    name = models.CharField(max_length=255)
    summary = models.TextField()
    score = models.IntegerField()
    score_url = models.URLField()
    def __str__(self):
        album = (self.name, self.artist.name if self.artist else '(null)')
        return '{0} - {1}'.format(*album)

class Artist(models.Model):
    mbid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    bio = models.TextField()
    def __str__(self):
        return self.name

class Image(models.Model):
    small = models.URLField()
    large = models.URLField()

class Label(models.Model):
    mbid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Review(models.Model):
    album = models.ForeignKey('Album', blank=True, null=True)
    publisher = models.ForeignKey('Publisher', blank=True, null=True)
    summary = models.TextField()
    score = models.IntegerField()
    date = models.DateField()

class Track(models.Model):
    artist = models.ForeignKey('Artist', blank=True, null=True)
    album = models.ForeignKey('Album', blank=True, null=True)
    mbid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    duration = models.IntegerField()
    def __str__(self):
        return self.name
