from django.db import models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugModel(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(SlugModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Album(SlugModel):
    artist = models.ForeignKey('Artist', blank=True, null=True)
    image = models.ForeignKey('Image', blank=True, null=True)
    tags = TaggableManager()
    date = models.DateField()
    mbid = models.CharField(max_length=255, unique=True)
    popularity = models.FloatField(default=0.0)
    score = models.IntegerField(default=0)
    score_url = models.URLField()
    summary = models.TextField()
    spotify_id = models.CharField(max_length=255)
    spotify_url = models.URLField(blank=True)

    def __str__(self):
        album = (self.name, getattr(self.artist, 'name', '(None)'))
        return '{0} - {1}'.format(*album)


class Artist(SlugModel):
    image = models.ForeignKey('Image', blank=True, null=True)
    tags = TaggableManager()
    bio = models.TextField()
    bio_url = models.URLField()
    mbid = models.CharField(max_length=255, unique=True)
    familiarity = models.FloatField(default=0.0)
    spotify_id = models.CharField(max_length=255)
    spotify_url = models.URLField(blank=True)
    trending = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Image(BaseModel):
    large = models.URLField()
    mbid = models.CharField(max_length=255, unique=True)
    medium = models.URLField()
    small = models.URLField()


class Publisher(BaseModel):
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name


class Review(BaseModel):
    album = models.ForeignKey('Album', blank=True, null=True)
    publisher = models.ForeignKey('Publisher', blank=True, null=True)
    date = models.DateField()
    score = models.IntegerField()
    summary = models.TextField()
    url = models.URLField(unique=True)

    def __str__(self):
        review = (
            getattr(self.publisher, 'name', '(None)'),
            getattr(self.album, 'name', '(None)'),
            self.score
        )
        return '{0} - {1} - {2}'.format(*review)


class Track(BaseModel):
    album = models.ForeignKey('Album', blank=True, null=True)
    duration = models.IntegerField()
    mbid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=255)
    spotify_url = models.URLField(blank=True)

    def __str__(self):
        track = (getattr(self.album, 'name', '(None'), self.name)
        return '{0} - {1}'.format(*track)

