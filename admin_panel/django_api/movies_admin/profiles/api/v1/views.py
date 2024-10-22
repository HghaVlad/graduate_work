from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from profiles.serializers import ProfilesSerializer, ReviewSerializer
from profiles.models import Profile, Review

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


class ReviewsApiView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['profile'] = request.user.id
        return super().create(request, *args, **kwargs)


class ReviewsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user and request.user.id == instance.profile.id:
            return super().update(request, *args, **kwargs)

        raise PermissionDenied("You can't update this review")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user and request.user.id == instance.profile.id:
            return super().destroy(request, *args, **kwargs)

        raise PermissionDenied("You can't delete this review")