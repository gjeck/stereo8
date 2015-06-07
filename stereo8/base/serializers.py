from rest_framework import serializers
from haystack.models import SearchResult
from .models import (
    Album,
    Artist,
    Image,
    Publisher,
    Review,
    Track,
)


class AlbumSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Album


class AlbumIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchResult


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review


class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track


