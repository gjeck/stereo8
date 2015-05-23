from django.shortcuts import render
from django.views.generic import ListView
from base.models import Artist


class ArtistList(ListView):
    model = Artist



