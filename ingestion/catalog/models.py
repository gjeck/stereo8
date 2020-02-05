from django.db import models
from django.db.models import Avg
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


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

class TaggedAlbum(TaggedItemBase):
    content_object = models.ForeignKey('Album', on_delete=models.CASCADE)

class Album(SlugModel):
    artist = models.ForeignKey('Artist', models.SET_NULL, blank=True, null=True)
    image = models.ForeignKey('Image', models.CASCADE, blank=True, null=True)
    sonic_info = models.ForeignKey('SonicInfo', models.CASCADE, blank=True, null=True)
    tags = TaggableManager(through=TaggedAlbum)
    date = models.DateField()
    mbid = models.CharField(max_length=255, unique=True)
    popularity = models.FloatField(default=0.0)
    score = models.IntegerField(default=0)
    score_url = models.URLField()
    summary = models.TextField()
    spotify_id = models.CharField(max_length=255)
    spotify_url = models.URLField(blank=True, null=True)

    def update_sonic_info(self):
        if not self.sonic_info:
            self.sonic_info, created = SonicInfo.objects.update_or_create(
                mbid=self.mbid
            )
        tracks = Track.objects.filter(album__mbid=self.mbid)
        if tracks:
            SonicInfo.aggregate_sonic_info(self.sonic_info, tracks)
            self.sonic_info.save()
            self.save()

    def __str__(self):
        return self.name

class TaggedArtist(TaggedItemBase):
    content_object = models.ForeignKey('Artist', on_delete=models.CASCADE)

class Artist(SlugModel):
    image = models.ForeignKey('Image', models.CASCADE, blank=True, null=True)
    sonic_info = models.ForeignKey('SonicInfo', models.CASCADE, blank=True, null=True)
    tags = TaggableManager(through=TaggedArtist)
    bio = models.TextField()
    bio_url = models.URLField()
    mbid = models.CharField(max_length=255, unique=True)
    spotify_id = models.CharField(max_length=255)
    spotify_url = models.URLField(blank=True, null=True)

    def update_sonic_info(self):
        if not self.sonic_info:
            self.sonic_info, created = SonicInfo.objects.get_or_create(
                mbid=self.mbid
            )
        albums = Album.objects.filter(artist__mbid=self.mbid)
        if albums:
            SonicInfo.aggregate_sonic_info(self.sonic_info, albums)
            self.sonic_info.save()
            self.save()

    def __str__(self):
        return self.name


class Image(BaseModel):
    large = models.URLField(blank=True, null=True)
    mbid = models.CharField(max_length=255, unique=True)
    medium = models.URLField(blank=True, null=True)
    small = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.mbid


class Publisher(BaseModel):
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name


class Review(BaseModel):
    album = models.ForeignKey('Album', models.SET_NULL, blank=True, null=True)
    publisher = models.ForeignKey('Publisher', models.SET_NULL, blank=True, null=True)
    date = models.DateField(null=True)
    score = models.IntegerField()
    summary = models.TextField()
    url = models.URLField(unique=True)

    def __str__(self):
        return '{0}'.format(getattr(self.publisher, 'name', '(None)'))


class Track(BaseModel):
    album = models.ForeignKey('Album', models.SET_NULL, blank=True, null=True)
    sonic_info = models.ForeignKey('SonicInfo', models.CASCADE, blank=True, null=True)
    duration = models.IntegerField()
    mbid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=255)
    spotify_url = models.URLField(blank=True, null=True)
    popularity = models.FloatField(default=0.0)
    track_number = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class SonicInfo(BaseModel):
    acousticness = models.FloatField(default=0.0)
    danceability = models.FloatField(default=0.0)
    energy = models.FloatField(default=0.0)
    instrumentalness = models.FloatField(default=0.0)
    liveness = models.FloatField(default=0.0)
    loudness = models.FloatField(default=0.0)
    mbid = models.CharField(max_length=255, unique=True)
    speechiness = models.FloatField(default=0.0)
    tempo = models.FloatField(default=0.0)
    valence = models.FloatField(default=0.0)
    mode = models.IntegerField(null=True)

    @staticmethod
    def aggregate_sonic_info(s, agglist):
        s.acousticness = agglist.aggregate(
            avg_acousticness=Avg('sonic_info__acousticness')
        ).get('avg_acousticness') or 0.0
        s.danceability = agglist.aggregate(
            avg_danceability=Avg('sonic_info__danceability')
        ).get('avg_danceability') or 0.0
        s.energy = agglist.aggregate(
            avg_energy=Avg('sonic_info__energy')
        ).get('avg_energy') or 0.0
        s.instrumentalness = agglist.aggregate(
            avg_instrumentalness=Avg('sonic_info__instrumentalness')
        ).get('avg_instrumentalness') or 0.0
        s.liveness = agglist.aggregate(
            avg_liveness=Avg('sonic_info__liveness')
        ).get('avg_liveness') or 0.0
        s.loudness = agglist.aggregate(
            avg_loudness=Avg('sonic_info__loudness')
        ).get('avg_loudness') or 0.0
        s.speechiness = agglist.aggregate(
            avg_speechiness=Avg('sonic_info__speechiness')
        ).get('avg_speechiness') or 0.0
        s.tempo = agglist.aggregate(
            avg_tempo=Avg('sonic_info__tempo')
        ).get('avg_tempo') or 0.0
        s.valence = agglist.aggregate(
            avg_valence=Avg('sonic_info__valence')
        ).get('avg_valence') or 0.0
        s.mode = agglist.aggregate(
            avg_mode=Avg('sonic_info__mode')
        ).get('avg_mode') or None

    def __str__(self):
        return self.mbid

