from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from profiles.serializers import ProfilesSerializer
from profiles.models import Profile

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




