from rest_framework.serializers import ModelSerializer
from .models import Profile, Bookmark


class ProfilesSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['id']


class BookmarkSerializer(ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'
        read_only_fields = ['id', "profile", "film"]
