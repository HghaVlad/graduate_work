from django.urls import path

from .views import ProfilesView, ProfilesDetailView, BookmarkApiView, BookmarkDetailView

urlpatterns = [
    path("profiles/", ProfilesView.as_view()),
    path("profile/<int:pk>/", ProfilesDetailView.as_view()),
    path("bookmarks/", BookmarkApiView.as_view()),
    path("bookmark/<int:pk>/", BookmarkDetailView.as_view()),
]
