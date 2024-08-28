from rest_framework import serializers

from django.db import transaction
from django.contrib.auth.hashers import make_password

from api.v1.user.models import User
from api.v1.board.models import Board, BoardCategory, BoardComment, BoardMedia

from api.common.utils import save_base64, read_base64


class BoardCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=32)

    def validate(self, data):
        return data

    def create(self, validated_data):
        return BoardCategory.actives.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

    class Meta:
        model = BoardCategory


class BoardCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.UUIDField(read_only=True)
    password = serializers.CharField(
        max_length=128, allow_blank=True, required=False, write_only=True
    )
    comment = serializers.CharField()
    parent_comment = serializers.PrimaryKeyRelatedField(
        queryset=BoardComment.actives.all(), allow_null=True
    )

    def validate(self, data):
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        board_id = self.context.get("view").kwargs.get("b_id")
        validated_data.update({"board_id": board_id})

        if user.is_anonymous:
            password = validated_data.pop("password", None)

            if password is None:
                raise Exception("익명사용자는 비밀번호가 필요합니다.")

            hashed_password = make_password(password)  # 비밀번호 해싱
            validated_data.update({"password": hashed_password})

            return BoardComment.actives.create(**validated_data)

        return BoardComment.actives.create(**validated_data, author=user)

    def update(self, instance, validated_data):
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        likes = instance.likes.count()
        ret.update({"likes": likes})

        return ret

    class Meta:
        model = BoardComment


class BoardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.UUIDField(read_only=True)
    password = serializers.CharField(
        max_length=128, allow_blank=True, required=False, write_only=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=BoardCategory.actives.all(), allow_null=True
    )  # 이렇게 하면 BoardCategory pk로 검색해서 넣어준다. 굳이 BoardCategorySerializer로 할 필요가 없다.
    title = serializers.CharField(max_length=128)
    text = serializers.CharField()
    views = serializers.IntegerField(read_only=True)
    is_secret = serializers.BooleanField(required=False)

    def validate(self, data):
        return data

    def create(self, validated_data):
        user = self.context["request"].user

        if user.is_anonymous:
            password = validated_data.pop("password", None)

            if password is None:
                raise Exception("익명사용자는 비밀번호가 필요합니다.")

            hashed_password = make_password(password)  # 비밀번호 해싱
            validated_data.update({"password": hashed_password})

            return Board.actives.create(**validated_data)

        return Board.actives.create(**validated_data, author=user)

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.category = validated_data.get("category", instance.category)
            instance.title = validated_data.get("title", instance.title)
            instance.text = validated_data.get("text", instance.text)
            instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        likes = instance.likes.count()
        ret.update({"likes": likes})

        comment = BoardComment.actives.filter(board=instance)
        comment_list = BoardCommentSerializer(instance=comment, many=True)
        ret.update({"comment": comment_list.data})

        media_objs = BoardMedia.actives.filter(board=instance)
        media_list = [media.filename for media in media_objs]
        ret.update({"media": media_list})

        return ret

    class Meta:
        model = Board
