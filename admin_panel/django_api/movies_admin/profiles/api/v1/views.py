from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from profiles.serializers import ProfilesSerializer, BookmarkSerializer
from profiles.models import Profile, Bookmark

# Create your views here.


class ProfilesView(ListCreateAPIView):
    serializer_class = ProfilesSerializer
    queryset = Profile.objects.all()


class ProfilesDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfilesSerializer
    queryset = Profile.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user and request.user.id == instance.id:
            return super().update(request, *args, **kwargs)

        raise PermissionDenied("You can't update this profile")


class BookmarkApiView(ListCreateAPIView):
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['profile'] = request.user.id
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        if Bookmark.objects.filter(profile=self.request.user,
                                   film_id=serializer.validated_data['film'].id).exists():
            raise PermissionDenied("You have already bookmarked this film")

        return super().perform_create(serializer)


class BookmarkDetailView(RetrieveDestroyAPIView):
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user and request.user.id == instance.profile.id:
            return super().destroy(request, *args, **kwargs)

        raise PermissionDenied("You can't delete this review")