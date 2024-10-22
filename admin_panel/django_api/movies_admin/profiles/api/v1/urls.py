from django.urls import path

from .views import ProfilesView, ProfilesDetailView

urlpatterns = [
    path("profiles/", ProfilesView.as_view()),
    path("profile/<int:pk>/", ProfilesDetailView.as_view()),
]
