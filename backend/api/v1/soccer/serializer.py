from rest_framework import serializers

from api.v1.soccer.models import Soccer, SoccerPlace, SoccerTime

from copy import deepcopy


class SoccerPlaceSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=False
    )  # 이렇게 해야 id로 조회, 수정이 가능하다.
    name = serializers.CharField(max_length=30)
    address = serializers.CharField(max_length=100)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def create(self, validated_data):
        latitude = validated_data.get("latitude")
        longitude = validated_data.get("longitude")

        try:
            where = SoccerPlace.objects.get(latitude=latitude, longitude=longitude)
        except SoccerPlace.DoesNotExist:
            where = SoccerPlace.objects.create(**validated_data)
        return where

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.save()
        return instance

    class Meta:
        model = SoccerPlace
        fields = "__all__"


class SoccerListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    where = SoccerPlaceSerializer(read_only=True)
    when = serializers.DateField(read_only=True)

    level = serializers.IntegerField(read_only=True)
    score = serializers.FloatField(read_only=True)

    class Meta:
        model = Soccer
        fields = ["id", "when", "where", "level", "score"]


class SoccerTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoccerTime
        fields = "__all__"


class SoccerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    where = SoccerPlaceSerializer()
    when = serializers.DateField()

    level = serializers.ChoiceField(choices=Soccer.Level)
    score = serializers.FloatField()
    memo = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, max_length=100
    )

    picture = serializers.ListField(
        required=False, allow_null=True, child=serializers.CharField()
    )
    video = serializers.ListField(
        required=False, allow_null=True, child=serializers.CharField()
    )
    tags = serializers.ListField(
        required=False, allow_null=True, child=serializers.CharField()
    )

    created_at = serializers.DateTimeField(
        required=False,
    )
    modified_at = serializers.DateTimeField(required=False, allow_null=True)
    deleted_at = serializers.DateTimeField(required=False, allow_null=True)

    def get_where(self, where_data):
        try:
            where = SoccerPlace.objects.get(id=where_data["id"])
        except Exception as e:
            where_serializer = SoccerPlaceSerializer(data=where_data)
            if where_serializer.is_valid(raise_exception=True):
                where = where_serializer.save()
        return where

    def create(self, validated_data):
        user = self.context["request"].user
        where = self.get_where(validated_data.pop("where"))
        return Soccer.objects.create(user=user, where=where, **validated_data)

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
        model = Soccer
        fields = "__all__"
        exclude = ["modified_at", "deleted_at"]
