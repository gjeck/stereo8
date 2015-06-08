from rest_framework import serializers
from taggit.models import Tag
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


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist


class BaseIndexSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    object = serializers.SerializerMethodField()
    score = serializers.FloatField()

    def get_object(self, obj):
        serializer_name = obj.model_name.capitalize() + 'Serializer'
        serializer_class = eval(serializer_name)
        serializer = serializer_class(obj.object)
        return serializer.data


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag


class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track


