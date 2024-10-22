from django.urls import path

from .views import ProfilesView, ProfilesDetailView, ReviewsApiView, ReviewsDetailView

urlpatterns = [
    path("profiles/", ProfilesView.as_view()),
    path("profile/<int:pk>/", ProfilesDetailView.as_view()),
    path("reviews/", ReviewsApiView.as_view()),
    path("review/<int:pk>/", ReviewsDetailView.as_view()),
]
