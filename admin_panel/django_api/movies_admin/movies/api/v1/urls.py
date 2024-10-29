from django.urls import path

from . import views


urlpatterns = [
    path('movies/', views.MoviesListApi.as_view()),
    path('movies/<uuid:pk>/', views.MoviesDetailApi.as_view(),),
    path("movies/<uuid:pk>/reviews", views.ReviewListCreateView.as_view()),
    path("reviews/<uuid:pk>/", views.ReviewDetailView.as_view()),
    path("reviews/<uuid:pk>/comments", views.CommentListCreateView.as_view()),
    path("comments/<uuid:pk>/", views.CommentDetailView.as_view()),
]
