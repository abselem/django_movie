from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    ActorListSerializer, 
    MovieListSerializer, 
    MovieDetailSerializer, 
    ReviewCreateSerializer, 
    CreateRatingSerializer, 
    CreateRatingSerializer,
    ActorDetailSerializer,
    )
from .service import PaginationMovies, get_client_ip, MovieFilter, PaginationMovies



class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = PaginationMovies 

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
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
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга к фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров или режиссеров"""
    queryset = Actor.objects.all()


    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer


# class MovieDetailView(generics.RetrieveAPIView):
#     """Вывод фильма"""

#     queryset = Movie.objects.filter(draft = False)
#     serializer_class = MovieDetailSerializer



# class ReviewCreateView(generics.CreateAPIView):
#     """Добавление отзыва к Фильму"""

#     serializer_class = ReviewCreateSerializer


# class AddStarRatingView(generics.CreateAPIView):
#     """Добавление рейтинга Фильму"""

#     serializer_class = CreateRatingSerializer


#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))


# class ActorListView(generics.ListAPIView):
#     """Вывод списка актеров"""

#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer


# class ActorDetailView(generics.RetrieveAPIView):
#     """Вывод актера или режиссера"""

#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer
