from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db import models
from .service import get_client_ip

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer,
    CreateRatingSerializer, ActorListSerializer, ActorDetailSerializer
)

class MovieListView(generics.ListAPIView):
    serializer_class = MovieListSerializer

    def get_queryset(self):
        # movies = Movie.objects.filter(draft=False).annotate(
        #     rating_user=models.Case(
        #         models.When(ratings__ip=get_client_ip(request), then=True),
        #         default=False,
        #         output_field=models.BooleanField()
        #     ),
        # )
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('rating__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer

class AddStarRatingView(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))

class ActorsListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

class ActorDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
