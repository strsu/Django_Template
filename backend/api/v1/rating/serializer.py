from rest_framework import serializers

from api.v1.rating.models import Movie


class NationSerilizer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, max_length=32
    )


class MovieRateTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rate_type_name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, max_length=32
    )


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    open = serializers.DateField()

    nation = NationSerilizer()

    created_at = serializers.DateTimeField(required=False)
    modified_at = serializers.DateTimeField(required=False, allow_null=True)
    deleted_at = serializers.DateTimeField(required=False, allow_null=True)

    def create(self, validated_data):
        where = self.get_where(validated_data.pop("where"))
        movie = Movie.objects.create(where=where, **validated_data)
        return movie

    def update(self, instance, validated_data):
        where = self.get_where(validated_data.pop("where"))
        instance.where = where

        instance.when = validated_data.get("when", instance.when)
        instance.level = validated_data.get("level", instance.level)
        instance.score = validated_data.get("score", instance.score)
        instance.memo = validated_data.get("memo", instance.memo)
        instance.picture = validated_data.get("picture", instance.picture)
        instance.tags = validated_data.get("tags", instance.tags)
        instance.save()
        return instance

    class Meta:
        model = Movie
        fields = "__all__"
        exclude = ["modified_at", "deleted_at"]
