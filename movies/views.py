from rest_framework import generics, permissions, viewsets
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from .service import get_client_ip, MovieFilter

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer,
    CreateRatingSerializer, ActorListSerializer, ActorDetailSerializer
)

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer

class ReviewCreateViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewCreateSerializer

class AddStarRatingViewSet(viewsets.ModelViewSet):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))

class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer

# class MovieListView(generics.ListAPIView):
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         # movies = Movie.objects.filter(draft=False).annotate(
#         #     rating_user=models.Case(
#         #         models.When(ratings__ip=get_client_ip(request), then=True),
#         #         default=False,
#         #         output_field=models.BooleanField()
#         #     ),
#         # )
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         return movies
#
#
# class MovieDetailView(generics.RetrieveAPIView):
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
#
# class ReviewCreateView(generics.CreateAPIView):
#     serializer_class = ReviewCreateSerializer
#
# class AddStarRatingView(generics.CreateAPIView):
#     serializer_class = CreateRatingSerializer
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))
#
# class ActorsListView(generics.ListAPIView):
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer
#
# class ActorDetailView(generics.RetrieveAPIView):
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer
