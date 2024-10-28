from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from profiles.serializers import ProfilesSerializer, BookmarkSerializer
from profiles.models import Profile, Bookmark
from http import HTTPStatus
from rest_framework.response import Response

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
        data = dict(request.data)
        data['profile'] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTPStatus.CREATED, headers=headers)

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