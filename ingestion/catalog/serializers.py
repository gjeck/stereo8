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
        fields = '__all__' 


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__' 


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
        fields = '__all__' 


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = '__all__' 


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__' 


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__' 


class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = '__all__' 


