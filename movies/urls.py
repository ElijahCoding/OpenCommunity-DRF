from django.urls import path

from . import views

urlpatterns = [
    path("movie/", views.MovieViewSet.as_view({'get': 'list'})),
    path("movie/<int:pk>", views.MovieViewSet.as_view({'get': 'retrieve'})),
    path("review/", views.MovieViewSet.as_view({'post': 'create'})),
    path("rating/", views.MovieViewSet.as_view({'post': 'create'})),
    path("actors/", views.MovieViewSet.as_view({'get': 'list'})),
    path("actors/<int:pk>/", views.MovieViewSet.as_view({'get': 'retrieve'})),
]

# urlpatterns = [
#     path("movie/", views.MovieListView.as_view()),
#     path("movie/<int:pk>", views.MovieDetailView.as_view()),
#     path("review/", views.ReviewCreateView.as_view()),
#     path("rating/", views.AddStarRatingView.as_view()),
#     path("actors/", views.ActorsListView.as_view()),
#     path("actors/<int:pk>/", views.ActorDetailView.as_view()),
# ]
