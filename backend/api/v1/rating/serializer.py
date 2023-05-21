from rest_framework import serializers

from api.v1.rating.models import (
    Nation,
    Genre,
    Movie,
    MovieRating,
    MovieRateType,
    Actor,
    ActorRateType,
    ActorRating,
)


class NationSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Nation
        fields = "__all__"


class GenreSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ["deleted_at"]


class MovieRateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRateType
        fields = "__all__"


class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRating
        fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"
        exclude = ["modified_at", "deleted_at"]


class ActorRateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActorRateType
        fields = "__all__"


class ActorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActorRating
        fields = "__all__"
