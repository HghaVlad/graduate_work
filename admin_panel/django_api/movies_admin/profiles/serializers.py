from rest_framework.serializers import ModelSerializer
from .models import Profile, Review


class ProfilesSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['id']


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['id', "profile", "film"]